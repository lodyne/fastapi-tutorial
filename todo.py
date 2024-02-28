# * TO-DO LIST
from fastapi import FastAPI
from models import Todo

app = FastAPI()


@app.get("/")
async def main():
    return {"message": "hello world"}


@app.get("/todos")
async def get_todos():
    return todos


@app.get("/todos/{todo_id}")
async def get_todos(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": "Not found"}


@app.delete("/todos/{todo_id}")
async def get_todos(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo has been deleted"}
    return {"message": "No todos found"}


@app.put("/todos/{todo_id}")
async def get_todos(todo_id: int, todo_obj: Todo):
    for todo in todos:
        if todo.id == todo_id:
            todo.id = todo_id
            todo.item = todo_obj.item
            return {"todo": todo}
    return {"message": "Not todos found to update"}


todos = []


@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo has been added"}
