from datetime import datetime
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel


# * TYPE HINTS
def name(first_name: str, last_name: str, age: int):
    return f"My name is {first_name.title()} {last_name.title()}.I am {age} years old."


print(name("lody", "mtui", "30"))


# * GENERIC TYPES/GENERIC
def get_list1(items: List[str]):
    # for item in items:
    print(items)


get_list1("hey")


def get_list2(items: list[str]):
    # for item in items:
    print(items)


get_list2("hey")


# * OPTIONAL AND UNION
def say(name: Optional[str] = None):
    if name:
        print("ndio")
    else:
        print("hAPANA")


say("lody")


def say_me(name: Union[str, None] = None):
    if name:
        print("ndio")
    else:
        print("hAPANA")


say_me()


# * NEW VERSION ~ ALTERNATIVES
def say_you(name: str | None = None):
    if name:
        print("ndio")
    else:
        print("hAPANA")


say("lody")


# * CLASS TYPES
class Student:
    def __init__(self, name: str):
        self.name = name


def get_student_name(student_name: Student):
    return student_name.name


student = Student("Lody Mtui")
print(get_student_name(student))


# * PYDANTIC MODELS
# Pydantic is a Python library to perform data validation
class Person(BaseModel):
    name: str
    age: int
    dob: datetime | None = None
    family: list[str] = []


data = {
    "name": "lody",
    "age": 20,
    "dob": "2017-06-01 12:22",
    "family": ["mama", "baba", "lui"],
}
person = Person(**data)
print(person)

# * METADATA ANNOTATIONS
"""
    Python also has a feature that allows putting 
    additional metadata in these type hints using Annotated.
"""


def hello_there(name: Annotated[str, "Nakusalimia tu"]):
    return name


print(hello_there("lui"))
