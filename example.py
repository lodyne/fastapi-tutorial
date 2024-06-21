from fastapi import FastAPI

app = FastAPI()

app.get("/world")
async def get_example():
    return "Hello"