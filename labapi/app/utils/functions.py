import sys
import yaml
import pymongo
import pysftp
import os
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from app.config import TokenPayload, SystemUser, Employee, Admin, ProfileUserModel
from fastapi import APIRouter, Body, Request, HTTPException, status
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "secret" #os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = "secret" #os.environ['JWT_REFRESH_SECRET_KEY']
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow()+timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, token: str = Depends(reuseable_oauth)) -> ProfileUserModel:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = await request.app.mongodb["user"].find_one({"email": token_data.sub})
    if user:
        user["role"] = "customer"
    else:
        user: Union[dict[str, Any], None] = await request.app.mongodb["employee"].find_one({"email": token_data.sub})
        if user:
            user["role"] = "employee"
        else:
            user: Union[dict[str, Any], None] = await request.app.mongodb["admin"].find_one({"email": token_data.sub})
            if user:
                user["role"] = "admin"
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Could not find user",
                    )
    return ProfileUserModel(**user)


async def get_current_employee(request: Request, token: str = Depends(reuseable_oauth)) -> Employee:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    employee: Union[dict[str, Any], None] = await request.app.mongodb["employee"].find_one({"email": token_data.sub})
    if employee:
        return Employee(**employee)
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        return Employee(**user)


async def get_current_admin(request: Request, token: str = Depends(reuseable_oauth)) -> Admin:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    admin: Union[dict[str, Any], None] = await request.app.mongodb["admin"].find_one({"email": token_data.sub})
    if admin:
        return Admin(**admin)
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find admin",
            )


async def check_permission(request: Request, token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = await request.app.mongodb["superadmin"].find_one({"email": token_data.sub})
    #db.get(token_data.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(**user)


def mongo_conn(vm):
    # client_yaml = os.path.join("~/", "../config.yaml")
    client_yaml = "config.yaml"
    # get client specifications
    with open(client_yaml, 'r') as f:
        clients = yaml.load(f, Loader=yaml.FullLoader)
    cred = clients.get(vm)
    if cred.get("user") is not None:
        cs = "mongodb://" + cred.get("user") + ":" + cred.get("key") + "@" + cred.get("host")

    if cred.get("user") is None:
        cs = "mongodb://" + cred.get("host")

    cs
    client = pymongo.MongoClient(cs)
    return client


def sftp_conn():
    client_yaml = "../config.yaml"
    # get client specifications
    with open(client_yaml, 'r') as f:
        clients = yaml.load(f, Loader=yaml.FullLoader)
    adr_prod_ssh = clients.get("adr_prod_ssh")
    host = adr_prod_ssh.get("host")
    username = adr_prod_ssh.get("user")
    password = adr_prod_ssh.get("password")

    source_dir = "/home/administrator/MP_EmotionalEngine/setting/uploads/"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp_conn = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
    return sftp_conn

    # def september_auth(auth, user, pw):
    #  # get client specifications
    #    with open(client_yaml, 'r') as f:
    #        clients = yaml.load(f, Loader=yaml.FullLoader)
    #
    #    cred = clients.get(auth)
    #
    #    client = HTTPBasicAuth(user, pw)

    #  return client


# pivot wider mean of cleaned_value
def emo_aggregation(emo_kpidata):
    emo_kpi = emo_kpidata.pivot_table(index=['adr_time'], columns="type",
                                      values=['cleaned_value'], aggfunc="mean")  # .reset_index(["adr_time"])

    # rename re index
    emo_kpi.columns = ["emo_" + col[1] for col in emo_kpi.columns]
    emo_kpi = emo_kpi.rename_axis("adr_time").reset_index()
    emo_kpi["n"] = len(emo_kpidata["testPerson"].unique())

    # check
    emo_time = emo_kpi.adr_time.unique()
    adr_time = res0.adr_time.unique()
    check = all(item in adr_time for item in emo_time)
    print("emp_agg check: " + str(check))

    return emo_kpi


# check
def check_adr_time(adr_t, res_t):  # adr_t = res1["adr_time"] res_t = res0["adr_time"]

    if not max(adr_t) <= max(res_t):
        print("Data-Error: max(adr_t)is not low or equal max(res_t)")
        sys.exit(1)

    if not min(adr_t) >= min(res_t):
        print("Data-Error: min(adr_t)is not higher or equal min(res_t)")
        sys.exit(1)

    return None


def download_data_from_sftp(sftp_file_name, target_base_path):
    """
    Download AGF SENDDEF data from sftp server
    """
    client_yaml = "../config.yaml"
    # get client specifications
    with open(client_yaml, 'r') as f:
        clients = yaml.load(f, Loader=yaml.FullLoader)
    adr_prod_ssh = clients.get("adr_prod_ssh")
    host = adr_prod_ssh.get("host")
    username = adr_prod_ssh.get("user")
    password = adr_prod_ssh.get("password")
    source_dir = "/home/administrator/MP_EmotionalEngine/setting/uploads/"
    target_dir = target_base_path
    target_path = target_dir + sftp_file_name
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    loop_flag = 1
    while loop_flag > 0:
        try:
            conn = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
            with conn.cd(source_dir):
                if conn.isfile(sftp_file_name):
                    conn.get(sftp_file_name, target_path)
                else:
                    return False
            loop_flag = 0
        except:
            return False
    return True
