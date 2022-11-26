from motor.motor_asyncio import AsyncIOMotorClient
import os
from app.config import settings, UserOut, TokenSchema, SystemUser, UserAuth, DeleteUser
from app.src.order.models import OrderModel, UpdateOrderModel
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

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post('/create_order', summary="Create new order", response_model=UserOut)
async def create_order(order: OrderModel, request: Request, user: SystemUser = Depends(get_current_user)):
    # querying database to check if user already exist
    created_date = datetime.now()
    product = await request.app.mongodb["product"].find_one({"name": order.product_name})
    total_price = product.price * order.quantity
    order = {
        'user_id': user.id,
        'status': "open",
        'employee_id': order.employee_id,
        'created_date': created_date,
        "product_id": order.product_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        'price': total_price,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["order"].insert_one(order)
        print('result %s' % repr(result.inserted_id))
        return_info = {'order': order["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post create_order"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": user.id, "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
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


@router.post('/update_order', summary="Update an order", response_model=TokenSchema)
async def update_order(order: UpdateOrderModel, request: Request, user: SystemUser = Depends(get_current_user)):
    order_id = await request.app.mongodb["order"].find_one({"id": order.id})
    if order_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Order doesn't exist"
        )
    created_date = datetime.now()
    product = await request.app.mongodb["product"].find_one({"name": order.product_name})
    total_price = product.price * order.quantity
    order = {
        'user_id': user.id,
        'status': "open",
        'employee_id': order.employee_id,
        'created_date': created_date,
        "product_id": order.product_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        'price': total_price,
        'id': str(uuid4())
    }
    try:
        result = await request.app.mongodb["order"].insert_one(order)
        print('result %s' % repr(result.inserted_id))
        return_info = {'order': order["id"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_BAD_REQUEST,
            detail="Inserting the user to database failed!"
        )

    api_info = "post update_order"
    # log_content = filter_by
    ip = request.client.host
    log_info = {"user": order["id"], "api": api_info, "datetime": datetime.now(), "ip": ip, "addInfo": ""}
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


@router.get('/get_order_by', summary='Get details of currently logged in user', response_model=SystemUser)
async def get_order(order: OrderModel, request: Request, user: SystemUser = Depends(get_current_user)):
    if order.user_id:
        order_list = await request.app.mongodb["order"].find({"user_id": order.user_id})
    elif order.product_name:
        order_list = await request.app.mongodb["order"].find({"product_name": order.product_name})
    elif order.status:
        order_list = await request.app.mongodb["order"].find({"status": order.status})
    elif order.employee_id:
        order_list = await request.app.mongodb["order"].find({"employee_id": order.employee_id})
    api_info = "get Order"
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
    return order_list
