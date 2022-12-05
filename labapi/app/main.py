from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
#from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser
import uvicorn
from app.src.project.routers import router as project_router
from app.src.account.routers import router as account_router
from app.src.readapi.routers import router as readapi_router
from app.src.user.routers import router as user_router
from app.src.order.routers import router as order_router
from app.src.product.routers import router as product_router
from app.src.employee.routers import router as employee_router
#from apps.employee.routers import router as account_router


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/login', response_class=RedirectResponse, include_in_schema=False)
async def docs_login():
    return RedirectResponse(url='/accounts/login')


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL, username=settings.DB_USER, password=settings.DB_PASSWORD)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():    app.mongodb_client.close()


@app.get("/healthz")
# Liveness probe for kubernetes status service
def kubernetes_liveness_probe():
    return {"status": "healthy"}


# app.include_router(project_router, tags=["projects"], prefix="/project")
app.include_router(account_router, tags=["accounts"], prefix="/accounts")
# app.include_router(readapi_router, tags=["emotiondata"], prefix="/emotiondata")
app.include_router(user_router, tags=["user"], prefix="/user")
app.include_router(order_router, tags=["order"], prefix="/order")
app.include_router(employee_router, tags=["employee"], prefix="/employee")
app.include_router(product_router, tags=["product"], prefix="/product")
# app.include_router(account_router, tags=["accounts"], prefix="/accounts")

# conn = mongo_conn(vm="mpee")
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

"""
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/", response_description="Add new project")
async def create_project(request: Request, project: ProjectModel = Body(...)):
    project = jsonable_encoder(project)
    new_project = await request.app.mongodb["projects"].insert_one(project)
    created_project = await request.app.mongodb["projects"].find_one(
        {"_id": new_project.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_project)


@app.get("/items/{item_id}")
async def read_video(file_name: str):
    gridfsdb = conn["gridfs"]
    fs = gridfs.GridFS(gridfsdb)
    id = gridfsdb.fs.files.find_one({'file_name': file_name})["_id"]
    res = fs.get(id).read()
    def iterfile():  #
        yield from res
    # print(res)
    return StreamingResponse(iterfile(), media_type="video/mp4")
"""