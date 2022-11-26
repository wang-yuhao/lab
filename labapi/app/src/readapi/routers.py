from fastapi import APIRouter, Body, Request, HTTPException, status
from app.config import settings, UserOut, TokenSchema, SystemUser, UserAuth, Adrdata
from fastapi import FastAPI, status, HTTPException, Depends
from app.utils.functions import get_current_user
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


# response_model = Adrdata,
@router.get("/by_adr_id/{adr_id}", summary="Get adr data from Mediaplus Insights", response_description="get data by adr_id")
async def get_adrdata_from_mpi(adr_id: str, request: Request, user: SystemUser = Depends(get_current_user)):
    filter_by = {"adr_id": adr_id}
    fields = {"_id": 0}
    projects = await request.app.mongodb["exports"].find(filter_by, fields).to_list(length=10)
    if projects:
        # user_name = {"user": user}
        api_info = "get by_adr_id"
        # log_content = filter_by
        ip = request.client.host
        log_info = {"user": user.email, "api": api_info, "addInfo": adr_id, "datetime": datetime.now(), "ip": ip}
        try:
            result = await request.app.mongodb["log"].insert_one(log_info)
            print('result %s' % repr(result.inserted_id))
            # return_info = {'email': user["email"], 'id': user["id"]}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_BAD_REQUEST,
                detail="Inserting the user to database failed!"
            )

    # projects_dict = pd.DataFrame(projects).fillna(0).to_dict()
    return projects
