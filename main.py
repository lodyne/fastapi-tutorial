from datetime import datetime, time, timedelta
from enum import Enum
from typing import Annotated, Literal, Optional, Union
from uuid import UUID
from fastapi import (
    Body,
    Cookie,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
    Header,
    Path,
    Query,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException as StarleteHTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, EmailStr, Field, HttpUrl

app = FastAPI()


#: PATH PARAMS
@app.get("/items/{id}")
async def main(id: int):
    return {"mimi": id}


@app.get("/mimi/lody")
async def name():
    return "This is my name"


@app.get("/mimi/{name}")
async def say_my_name(name: str):
    return {"JINA": name}


fake_items_db = [
    {"name": "Bar"},
    {"name": "Baz"},
    {"name": "Bax"},
]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/hey/{item_id}")
async def get_item_id(item_id: str, query: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if query:
        item.update({"query": query})
        # return {"item_d":item_id,"query":query}
    if not short:
        item.update({"description": "mimi ndie"})

    return item
    # return {"item_id":item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_id(
    user_id: int, item_id: str, query: str | None = None, short: bool = False
):
    item = {"item_d": item_id, "owner": user_id}
    if query:
        item.update({"query": query})
        # return {"item_d":item_id,"query":query}
    if not short:
        item.update({"description": "mimi ndie"})

    return item


# * Path Parameters and Numeric Validation
@app.get("/valid/{user_id}")
async def read_validation(
    user_id: int = Path(  # ? Path Field used by Path Params
        ..., title="ID for user id", description="USER ID"
    ),
    query: str | None = Query(None, alias="user-query"),
):
    results = {"user_id": user_id}
    if query:
        results.update({"query": query})
    return results


# ! use of * to solve non-default argument follows default argument, problem
"""Ellipsis (...) is used to mark the field as required"""


@app.get("/again/{user_id}")
async def read_again(
    *,
    user_id: int = Path(
        ..., title="ID for user id", description="USER ID", lt=15, gt=10
    ),
    query: str,
):
    results = {"user_id": user_id}
    if query:
        results.update({"query": query})
    return results


# ! if you use Annotated, no need of *
""" Annotated is used to add extra metadata.
"""


@app.get("/again/{user_id}")
async def read_me_again(
    user_id: Annotated[
        int, Path(..., title="ID for user id", description="USER ID", lt=15, gt=10)
    ],
    query: str,
):
    results = {"user_id": user_id}
    if query:
        results.update({"query": query})
    return results


#: QUERY PARAMS
@app.get("/read")
async def read_me(query: str | None = None):
    result = {"items": [{"items_id": "fool"}, {"items_id": "bass"}]}
    if query:
        result.update({"query": query})
    return result


# * Query Parameters and String Validation
@app.get("/readyou")
async def read_you(query: str = Query("fixed", min_length=3, max_length=10)):
    result = {"items": [{"items_id": "fool"}, {"items_id": "bass"}]}
    if query:
        result.update({"query": query})
    return result


@app.get("/readwe")
async def read_we(
    query: str | None = Query(  # ? Query Field used by Query Params
        ...,
        min_length=5,
        max_length=12,
        title="Mimi",
        description="My First FAST API",
        alias="query-item",
    )
):
    result = {"items": [{"items_id": "fool"}, {"items_id": "bass"}]}
    if query:
        result.update({"query": query})
    return result


@app.get("/read/hidden")
async def hidden(hidden: str | None = Query(None, include_in_schema=False)):
    if hidden:
        return {"hidden": hidden}
    return {"hidden": "Not found"}


#: REQUEST BODY
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


#: BODY-MULTIPLE PARAMS
@app.post("/items/item_id")
async def create_item_with_mutiple(item_id: int, item: Item, query: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if query:
        result.update({"query": query})
    return result


#: BODY NESTED MODELS
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(None, title="The description")
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: list[Image] | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: Item


# class Importance(BaseModel):
#     importance:int


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="This is Id", ge=0, le=10),
    query: str | None = None,
    # item: Item,
    item: Item = Body(..., embed=True),  # ? Body Field used by Request Body
    # user:User,
    # importance: int = Body(...)
    # importance:Importance
):
    results = {"item_id": item_id}
    if query:
        results.update({"query": query})
    if item:
        results.update({"item": item})
    # if user:
    #     results.update({"user":user})
    # if importance:
    #     results.update({"importance":importance})
    return results


@app.post("/offers")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer


#: DECLARE REQUEST EXAMPLE DATA
"""You can declare examples for a Pydantic model 
    that will be added to the generated JSON Schema.
"""

# * METHOD 1


class Build1(BaseModel):
    name: str
    description: str

    model_config = {
        "json_schema_extra": {"examples": [{"name": "House", "description": "luxury"}]}
    }
    # ! outdated - used for pydantic v1
    # class Config:
    #     schema_extra = {
    #         "examples":[
    #             {
    #             "name":"House",
    #             "description":"luxury"
    #             }
    #         ]
    #     }


@app.put("/build1/{item_id}")
async def update_build_method1(item_id: int, item: Build1):
    results = {"item_id": item_id, "item": item}
    return results


# * METHOD 2
class Build2(BaseModel):
    name: str = Field(..., example="House")
    description: str = Field(..., example="luxury one")


@app.put("/build2/{item_id}")
async def update_build_method2(item_id: int, item: Build2):
    results = {"item_id": item_id, "item": item}
    return results


# * METHOD 3
class Muscle(BaseModel):
    name: str
    description: str


@app.put("/muscle/{item_id}")
async def build_muscle(
    item_id: int,
    muscle: Muscle = Body(..., example={"name": "lui", "description": "hello"}),
):
    results = {"item_id": item_id, "muscle": muscle}
    return results


# * METHOD 4
@app.put("/flexmuscle/{item_id}")
async def flex_muscle(
    item_id: int,
    muscle: Muscle = Body(
        ...,
        openapi_examples={
            "normal": {
                "summary": "An example of normal data",
                "description": "Normal FAST API",
                "value": {"name": "House", "description": "house of luxury"},
            },
            "converted": {
                "summary": "An example of converted data",
                "description": "Converted  FAST API",
                "value": {"name": "House", "description": "house of luxury"},
            },
            "invalid": {
                "summary": "Rejected data",
                "description": "Describe Invalidation",
                "value": {"name": "store", "description": "hardship "},
            },
        },
    ),
):
    results = {"item_id": item_id, "muscle": muscle}
    return results


#: EXTRA DATA TYPES
@app.put("/readitems/{item_id}")
async def read_items(
    item_id: UUID,
    start_date: datetime | None = Body(None, embed=True),
    end_date: datetime | None = Body(None),
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None),
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "item_id": item_id,
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


#: COOKIE AND HEADERS PARAMS
@app.put("/readcookie/")
async def cookie_header(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None, convert_underscores=False),
    accept: str | None = Header(None),
    accept_langauge: str | None = Header(None),
    user_agent: str | None = Header(None),
):
    return {
        "cookie_id": cookie_id,
        "accept_encoding": accept_encoding,
        "accept": accept,
        "accept_langauge": accept_langauge,
        "user_agent": user_agent,
    }


#: RESPONSE MODELS
class Person(BaseModel):
    name: str
    age: int
    description: str | None = None
    price: int | None = None
    tax: int = 10.5


person = {
    "foo": {"name": "Lod", "age": 30, "description": "Mimi"},
    "faz": {
        "name": "Lod",
        "age": 30,
        "description": "This is me",
        "price": 200,
        "tax": 13,
    },
    "bar": {
        "name": "Lui",
        "age": 20,
        "description": "This is me",
        "price": 100,
        "tax": 15,
    },
}


@app.put("/describe/", response_model=Person)
async def describe_me(person: Person):
    return {"person", person}


@app.get("/person/{item_id}", response_model=Person, response_model_exclude_unset=True)
async def personification(item_id: Literal["foo", "faz", "bar"]):
    return person[item_id]


@app.get(
    "/person/{item_id}/name",
    response_model=Person,
    response_model_include={"name", "description"},
)
async def include_person(item_id: Literal["foo", "faz", "bar"]):
    return person[item_id]


@app.get(
    "/person/{item_id}/public", response_model=Person, response_model_exclude={"tax"}
)
async def exclude_person(item_id: Literal["foo", "faz", "bar"]):
    return person[item_id]


class UserBase(BaseModel):
    name: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


@app.post("/userin/", response_model=UserOut)
async def user_in(user_in: UserIn):
    return user_in


#: EXTRA MODELS
class UserInside(UserBase):
    password: str


class UserOutside(UserBase):
    pass


class UserDB(BaseModel):
    hashed_password: str


def fake_hashed_password(raw_password: str):
    return f"supersecret {raw_password}"


def fake_save_user(user_in=UserInside):
    hashed_password = fake_hashed_password(user_in.password)
    user_in_db = UserDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User save")
    return user_in_db


@app.post("/userdb/", response_model=UserOutside)
async def create_user_db(user_in: UserInside):
    user_saved = fake_save_user(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "Ride this car", "type": "car"},
    "item2": {"description": "Fly this plane", "type": "plane", "size": 9},
}


@app.get("/car/plane/{item_id}", response_model=Union[PlaneItem, CarItem])
async def make_a_base(item_id: Literal["item1", "item2"]):
    return items[item_id]


class SingleItem(BaseModel):
    name: str
    description: str


items2 = [
    {"description": "Ride this car", "name": "car"},
    {"description": "Fly this plane", "name": "plane"},
]


@app.get("/single", response_model=list[SingleItem])
async def single_item():
    return items2


@app.get("/arbitrary/", response_model=dict[str, int])
async def arbitrary_dictionary():
    return {"key": 9, "value": 8}


#: RESPONSE STATUS CODES
@app.get("/status/", status_code=201)
async def show_status_codes(name: str):
    return {"name": name}


@app.delete("/items/{pk}", status_code=204)
async def delete_item(pk: str):
    return {"pk": pk}


@app.get("/redirect", status_code=301)
async def redirect_items():
    return {"hello": "world"}


@app.get("/found", status_code=401)
async def not_found_items():
    return {"hello": "world"}


# * you can use this by: - from fastapi import status
@app.get("/status/{name}", status_code=status.HTTP_201_CREATED)
async def not_found_items(name: str):
    return {"name": name}


#: FORM DATA
class UserProfile(BaseModel):
    name: str
    password: str


@app.post("/login/")
async def login(user: UserProfile):
    return user


@app.post("/login/{name}")
async def login_json(username: str = Body(...), password: str = Body(...)):
    results = {"username": username, "password": password}
    return results


@app.post("/signin/")
async def signin(username: str = Form(...), password: str = Form(...)):
    results = {"username": username, "password": password}
    return results


#: REQUEST FILES
@app.post("/files")
async def post_files(files: list[bytes] = File(...)):
    return {"file": [len(file) for file in files]}


@app.post("/uploadfiles")
async def upload_files(file: UploadFile | None = None):
    if not file:
        return f"No file found"
    return {"file": file.filename}


#: REQUEST FORMS AND FILES


@app.post("/formsipload/")
async def create_forms_file(
    file1: bytes = File(...),
    file2: UploadFile = File(...),
    token: str = Form(...),
    hello: str = Body(...),
):
    return {
        "file_size": len(file1),
        "file_content_type": file2.content_type,
        "token": token,
        "hello": hello,
    }


class SubGeneral(BaseModel):
    name: str
    url: HttpUrl


#: HANDLING ERRORS
items = {"sms": "The message"}


@app.get("/handling_errors/{item_id}")
async def handling_errors(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found",
            headers={"X-Error": "This is my error"},
        )

    return {"item": items[item_id]}


class UnicornExeption(Exception):
    def __init__(self, name):
        self.name = name
        super(UnicornExeption, self).__init__(name)


@app.exception_handler(UnicornExeption)
async def unicorn_exception_handler(request: Request, exc: UnicornExeption):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Ohoooo {exc.name} did someting wrong"},
        headers={"EX-ERROR": "Exception Error"},
    )


@app.get("/unicorns/{name}")
async def read_unicorns(sms: str):
    if sms == "yolo":
        raise UnicornExeption(name=sms)
    return {"unicorn_name": sms}


@app.exception_handler(RequestValidationError)
async def validate_exception(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(StarleteHTTPException)
async def http_exception(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=400)


@app.get("/validation_items/{item_id}")
async def read_validation(item_id: int):
    if item_id == 3:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="Nothing was the same"
        )
    return {"item_id": item_id}


@app.exception_handler(RequestValidationError)
async def validation_request(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item2(BaseModel):
    title: str
    size: int


@app.post("/new_items")
async def create_new_items(item: Item2):
    return item


# * Re-use FastAPI's exception handlers
"""
i.e. http_exception_handler & request_validation_exception_handler
"""


@app.exception_handler(StarleteHTTPException)
async def custom_http_exception(request, exc):
    print(f"Error Server: Error in the server as in {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def custom_http_validation(request, exc):
    print(f"Invalid data:The client has invalid data as in  {repr(exc)}")
    return await request_validation_exception_handler(request, exc)


@app.get("/blah_items/{item_id}")
async def read_validation(item_id: int):
    if item_id == 3:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="3 is not magic number"
        )
    return {"item_id": item_id}


# : PATH OPERATION CONFIGURATION
class Item3(BaseModel):
    name: str
    description: str
    price: int
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    new = "items"
    path = "users"


@app.post(
    "/path_items/",
    response_model=Item3,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.new],
    summary="Create an item",
    # description="Create an item with all the information",
    response_description="Create items",
)
async def create_new_item_one(item: Item3):
    """
    Create an item with all the information
    - **name**: a name of an item
    - **description**: an item description
    - **price**: an item price
    - **tax**: tax payable
    - **tags**: a unique string for the item

    """
    return item


@app.get("/read_new_items/", tags=["NEW"])
async def read_new_items():
    return {"name": "Lody", "price": 988}


@app.get("/get_new_items/", tags=["PATH"])
async def get_new_items():
    return [{"resource": "Watu", "speciality": "Engineers"}]


@app.get("/read_new_items2/", tags=[Tags.new])
async def read_new_items():
    return {"name": "Lody", "price": 988}


@app.get("/get_new_items2/", tags=[Tags.path])
async def get_new_items():
    return [{"resource": "Watu", "speciality": "Engineers"}]


@app.get("/deprecated_items/", tags=["deprecated"], deprecated=True)
async def read_new_items():
    return {"name": "Lody", "price": 988}


# : JSON COMPATIBLE ENCODER AND BODY UPDATES
fake_db = {}


class Item4(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


class Item5(BaseModel):
    name: str | None = None
    age: int | None = None
    description: str | None = None
    price: int | None = None
    tax: float = 10.4


fake_items = {
    "foo": {"name": "Lod", "age": 30, "description": "Mimi"},
    "faz": {
        "name": "Lod",
        "age": 30,
        "description": "This is me",
        "price": 200,
        "tax": 13,
    },
    "bar": {
        "name": "Lui",
        "age": 20,
        "description": "This is me",
        "price": 100,
        "tax": 15,
    },
}


@app.put("/jsonitem/{id}")
async def json_item_encoder(id: str, item: Item4):
    json_compatible_items = jsonable_encoder(item)
    fake_db[id] = json_compatible_items
    print(fake_db)
    return "Success"


@app.get("/json_items/{item_id}", response_model=Item5)
async def json_red_items(item_id: str):
    return fake_items.get(item_id)


@app.put("/json_items/{item_id}", response_model=Item5)
async def json_red_items(item_id: str, item: Item5):
    update_items = jsonable_encoder(item)
    fake_items[item_id] = update_items
    return update_items


@app.patch("/json_items/{item_id}", response_model=Item5)
async def json_red_items(item_id: str, item: Item5):
    stored_items = fake_items.get(item_id)
    if stored_items is not None:
        fake_items_model = Item5(**stored_items)
    else:
        fake_items_model = Item5()
    update_data = item.model_dump(exclude_unset=True)
    updated_item = fake_items_model.model_copy(update=update_data)
    fake_items[item_id] = jsonable_encoder(updated_item)
    print(fake_items)
    return updated_item


# : DEPENDENCIES
# * Introduction
async def hello_world():
    """Dependencies
    You can nest dependencies
    """
    return f"HELLO WORLD"


async def common_parameters(
    query: str | None = None,
    skip: int = 0,
    limit: int = 100,
    sms: str = Depends(hello_world),
):
    return {"query": query, "skip": skip, "limit": limit, "message": sms}


@app.get("/item_dependencies")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"commons": commons}


@app.get("/user_dependencies")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# * Classes as Dependencies

faker_items_db = [
    {"name": "Bar"},
    {"name": "Baz"},
    {"name": "Foo"},
]


class CommonQueryParams:
    def __init__(
        self, item_id: int, query: str | None = None, skip: int = 0, limit: int = 100
    ) -> None:
        self.item_id = item_id
        self.query = query
        self.skip = skip
        self.limit = limit

        """Class Dependencies
            it  can work with path params, query params etc.
        """


# * METHOD 1
@app.get("/read_class_items1/{item_id}")
async def read_class_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    print(commons.item_id)
    if commons.query:
        response.update({"query": commons.query})
    items = faker_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# * METHOD 2
@app.get("/read_class_items2/{item_id}")
async def read_class_items(commons=Depends(CommonQueryParams)):
    response = {}
    print(commons.item_id)
    if commons.query:
        response.update({"query": commons.query})
    items = faker_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# * METHOD 3
@app.get("/read_class_items3/{item_id}")
async def read_class_items(commons: CommonQueryParams = Depends()):
    response = {}
    print(commons.item_id)
    if commons.query:
        response.update({"query": commons.query})
    items = faker_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# : SUB-DEPENDENCIES
def query_extractor(query: str | None = None):
    return query


def query_or_body_extractor(
    query: str = Depends(query_extractor), last_query: str | None = Body(None)
):
    if not query:
        return last_query
    return query


@app.post("/query_subdependecies/")
async def try_query(query: str = Depends(query_or_body_extractor)):
    return query


# : DEPENDENCIES IN PATH OPERATION DECORATORS
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-hashed-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token Header Invalid"
        )
    return "hello"


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-hashed-key":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token Header Invalid"
        )
    return x_key


@app.get("/pathitems/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def path_item(query: str = Depends(verify_token)):
    return [{"item": "Fooo"}, {"item": "Baz"}]


# * global dependencies
"""You can use global dependencies as follows:- 

    app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
    
"""


@app.get("/useritems/")
async def path_item():
    return [{"item": "Fooo"}, {"item": "Baz"}]


# : SECURITY

fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="fakehashedsecret",
        disabled=False,
    ),
    "alice": dict(
        username="alice",
        full_name="Alice Wonderson",
        email="alice@example.com",
        hashed_password="fakehashedsecret2",
        disabled=True,
    ),
}


def fake_hash_password(password: str):
    return f"fakehashed{password}"


class User1(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_fake_decode(token):
    return User(
        username=f"{token}fakedecoded", email="foo@example.com", full_name="Lody"
    )


oauth = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth)):
    user = get_fake_decode(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication credentials",
            headers={"www-Aunthenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "Bearer"}


@app.get("/security_user")
async def get_user(user: User = Depends(get_current_active_user)):
    return user


@app.get("/security_path")
async def read_items(token: str = Depends(oauth)):
    return {"token": token}


# :PLAYGROUND
class General(BaseModel):
    name: str = Field(..., description="This is name", title="NAME", examples=["Lui"])
    age: int = Field(..., description="This is age", title="AGE", example="12")
    description: str | None = None
    sub_general: SubGeneral


class Department(BaseModel):
    head: str | None = None
    general: General


def get_user(user: str):
    return {"user": user}


@app.post("/general/{id}/", status_code=status.HTTP_201_CREATED)
async def general_route(
    *,
    user: str = Depends(get_user),
    id: int = Path(
        title="IDENTIFICATION",
        description="This is identification",
        example=123,
    ),
    query: str = Query(
        ..., title="QUERY PARAMS", description="This is query params", example="hello"
    ),
    department: list[Department] = Body(..., embed=True),
    # request: General | None = Body(embed=True),
    # username: str = Form(...),
    # password: str = Form(...),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="User is required"
        )
    return {
        "id": id,
        "query": query,
        "department": department,
        "user": user,
        # "request": request,
        # "password": password,
        # "username": username,
    }


# : SQL RELATIONAL DATABASE
