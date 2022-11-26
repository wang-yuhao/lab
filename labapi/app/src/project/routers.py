from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import ProjectModel, UpdateProjectModel

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.get("/", response_description="list all projects id")
async def list_projects(request: Request):
    fields = "adr_id"
    projects = await request.app.mongodb["rawdata"].distinct(fields)
    return projects



