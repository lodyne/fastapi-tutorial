from fastapi import Depends, FastAPI
# from .routers.users import router as user_router
# from .routers.items import router as item_router

from .routers import user_router
from .routers import item_router
# from .routers import users,items

from sub_app.dependecies import get_query_token

app = FastAPI(dependencies=[Depends(get_query_token)])




@app.get("/")
async def root():
    return {"message": "Hello Big Team"}

app.include_router(user_router)
app.include_router(item_router)

# app.include_router(users.router)
# app.include_router(items.router)