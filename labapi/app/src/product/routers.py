from motor.motor_asyncio import AsyncIOMotorClient
import os
from app.config import settings, UserOut, TokenSchema, SystemUser, UserAuth, DeleteUser
from app.src.product.models import ProductModel, UpdateProductModel
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
    get_current_employee,
    check_permission
)

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post('/create_product', summary="Create new product", response_model=ProductModel)
async def create_product(product: ProductModel, request: Request, employee: SystemUser = Depends(get_current_employee)):
    # querying database to check if user already exist
    created_date = datetime.now()
    product = await request.app.mongodb["product"].find_one({"name": product.product_name})
    total_price = product.price * product.quantity
    product = {
        'status': "open",
        'employee_id': product.employee_id,
        'created_date': created_date,
        "product_id": product.product_id,
        "product_name": product.product_name,
        'price': total_price,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["product"].insert_one(product)
        print('result %s' % repr(result.inserted_id))
        return_info = {'product': product["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post create_product"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": employee.id, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
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


@router.post('/update_product', summary="Update an product", response_model=TokenSchema)
async def update_product(product: UpdateProductModel, request: Request, user: SystemUser = Depends(get_current_employee)):
    product = await request.app.mongodb["product"].find_one({"id": product.id})
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This product doesn't exist"
        )
    created_date = datetime.now()
    product = await request.app.mongodb["product"].find_one({"name": product.product_name})
    total_price = product.price * product.quantity
    product = {
        'user_id': user.id,
        'status': "open",
        'employee_id': product.employee_id,
        'created_date': created_date,
        "product_id": product.product_id,
        "product_name": product.product_name,
        "quantity": product.quantity,
        'price': total_price,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["product"].insert_one(product)
        print('result %s' % repr(result.inserted_id))
        return_info = {'product': product["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post update_product"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": product["id"], "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
    try:
        result = await request.app.mongodb["log"].insert_one(log_info)
        print('result %s' % repr(result.inserted_id))
        # return_info = {'email': user["email"], 'id': user["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )
    return product


@router.get('/get_product_by', summary='Get details of the product.', response_model=SystemUser)
async def get_product(product: ProductModel, request: Request, user: SystemUser = Depends(get_current_user)):
    if product.product_name:
        product = await request.app.mongodb["product"].find_one({"product_name": product.product_name})
    elif product.status:
        product = await request.app.mongodb["product"].find_one({"status": product.status})
    elif product.employee_id:
        product = await request.app.mongodb["product"].find_one({"employee_id": product.employee_id})
    api_info = "get product"
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
            detail="Get the product from database failed!"
        )
    return product
