from motor.motor_asyncio import AsyncIOMotorClient
import os
print(os.getcwd())
from app.config import settings, UserOut, TokenSchema, SystemUser, UserAuth, DeleteUser, Admin, Employee
from app.src.user.models import UserModel, UpdateUserModel
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
    get_current_employee,
    get_current_admin,
    check_permission
)

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post('/create_employee', summary="Create new employee", response_model=Employee)
async def create_employee(data: Employee, request: Request, admin: Admin = Depends(get_current_admin)):
    # querying database to check if employee already exist
    employee_email = await request.app.mongodb["employee"].find_one({"email": data.email})
    employee_phone = await request.app.mongodb["employee"].find_one({"phone": data.email})
    if (employee_email is not None) and (employee_phone is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee with this email or Phone number already exist"
        )
    created_date = datetime.now()
    employee = {
        'email': data.email,
        'status': "active",
        'password': get_hashed_password(data.password),
        'name': data.name,
        'phone_number': data.phone_number,
        'gender': data.gender,
        'product_list': [],
        'birth_date': data.birth_date,
        'created_date': created_date,
        'country': data.country,
        'ort': data.ort,
        'last_login': created_date,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["employee"].insert_one(employee)
        print('result %s' % repr(result.inserted_id))
        return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the employee to database failed!"
        )

    api_info = "post create_account"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"employee": employee.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the log information to database failed!"
        )
    return return_info

@router.post('/update_employee', summary="Create new employee", response_model=Employee)
async def update_employee(data: Employee, request: Request, admin: Admin = Depends(get_current_admin)):
    # querying database to check if employee already exist
    employee_email = await request.app.mongodb["employee"].find_one({"email": data.email})
    #employee_phone = await request.app.mongodb["employee"].find_one({"phone": data.email})
    # if (employee_email is not None) and (employee_phone is not None):
    if (employee_email is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="employee with this email or Phone number already exist"
        )
    created_date = datetime.now()
    employee = {
        'email': data.email,
        'status': "active",
        'password': get_hashed_password(data.password),
        'name': data.name,
        'phone_number': data.phone_number,
        'gender': data.gender,
        'product_list': [],
        'birth_date': data.birth_date,
        'created_date': created_date,
        'country': data.country,
        'ort': data.ort,
        'last_login': created_date,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["employee"].insert_one(employee)
        print('result %s' % repr(result.inserted_id))
        return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the employee to database failed!"
        )

    api_info = "post create_account"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"employee": employee.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the log information to database failed!"
        )
    return return_info

@router.post('/login', summary="Create access and refresh tokens for employee", response_model=TokenSchema)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    employee = await request.app.mongodb["employee"].find_one({"email": form_data.username})
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = employee['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    api_info = "post employee login"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"employee": employee["email"], "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the employee to database failed!"
        )
    return {
        "access_token": create_access_token(employee['email']),
        "refresh_token": create_refresh_token(employee['email']),
    }


@router.get('/profile', summary='Get details of currently logged in employee', response_model=Employee)
async def get_me(request: Request, employee: Employee = Depends(get_current_employee)):
    api_info = "get profile"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"employee": employee.email, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': employee["email"], 'id': employee["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the employee to database failed!"
        )
    return employee
