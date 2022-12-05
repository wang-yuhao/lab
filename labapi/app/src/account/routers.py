from motor.motor_asyncio import AsyncIOMotorClient
import os
print(os.getcwd())
from app.config import settings, UserOut, TokenSchema, SystemUser, UserAuth, DeleteUser
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from uuid import uuid4
from datetime import datetime
from app.utils.functions import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_user,
    check_permission
)
from app.src.user.models import UserModel, UpdateUserModel, CreateUserModel, ResponseUserModel, ProfileUserModel, UserLoginModel
import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post('/create_account', summary="Create new user", response_model=TokenSchema)
async def create_user(data: CreateUserModel, request: Request):
# async def create_user(data: UserAuth, request: Request, user: SystemUser = Depends(get_current_user)):
    """
    if user.role == "User":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account does not have permission to use this feature."
        )

    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    """
    # querying database to check if user already exist
    user = await request.app.mongodb["admin"].find_one({"email": data.email})
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    created_date = datetime.now()
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'name': data.name,
        'phone_number': data.phone_number,
        'gender': data.gender,
        'birth_date': data.birth_date,
        'created_date': created_date,
        'country': data.country,
        'ort': data.ort,
        'last_login': created_date,
        'id': str(uuid4())
    }
    try:
        print("user: ", user)
        result = await request.app.mongodb["admin"].insert_one(user)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post create_account"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": data.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the log information to database failed!"
        )
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }


@router.put('/delete_account', summary="Delete a user", response_model=UserOut)
async def create_user(data: DeleteUser, request: Request, user: SystemUser = Depends(get_current_user)):
    if user.role == "User":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account does not have permission to use this feature."
        )
    # querying database to check if user already exist
    user = await request.app.mongodb["admin"].find_one({"email": data.email})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email does not exist"
        )
    try:
        result = await request.app.mongodb["admin"].delete_one({'email': data.email})
        #print('result %s' % repr(result.inserted_id))
        return_info = {'email': data.email, 'id': user.id}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "put delete_account"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": user.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the log information to database failed!"
        )
    return return_info

"""
@router.post('/super_admin_signup', summary="Create new user", response_model=UserOut)
async def create_super_user(data: UserAuth, request: Request):
    # querying database to check if user already exist
    user = await request.app.mongodb["super_admin"].find_one({"email": data.email})
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["super_admin"].insert_one(user)
        print('result %s' % repr(result.inserted_id))
        return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post super_admin_signup"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": user.email, "api": api_info, "datetime": datetime.now(), "ip": ip}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )
    return return_info
"""


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await request.app.mongodb["super_admin"].find_one({"email": form_data.username})
    if user is None:
        user = await request.app.mongodb["admin"].find_one({"email": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    api_info = "post login"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": user["email"], "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }


@router.get('/profile', summary='Get details of currently logged in user', response_model=SystemUser)
async def get_me(request: Request, user: SystemUser = Depends(get_current_user)):
    api_info = "get profile"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": user.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )
    return user
