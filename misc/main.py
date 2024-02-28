from fastapi import FastAPI

from .routers import post,comment

app = FastAPI()

app.include_router(post.router)
app.include_router(comment.router)

@app.get("/")
async def root():
    return {"Hello":"World"}