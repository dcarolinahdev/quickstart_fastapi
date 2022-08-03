# Python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field
# FastAPI
from fastapi import FastAPI, Body, Query, Path, status

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Pasto"
        )
    state: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Nariño"
        )
    country: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="Colombia"
        )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Carolina"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Hernandez"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=30
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None,example=False)

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="m56H02zP"
    )

    """class Config:
        schema_extra = {
            "example": {
                "first_name": "Caro",
                "last_name": "Hernández",
                "age": 30,
                "hair_color": "black",
                "is_married": False
            }
        }"""

class PersonOut(PersonBase):
    pass

@app.get(
    path="/",
    status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        example="Susana",
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    # age: str = Query(...)
    age: Optional[int] = Query(
        0,
        example=25,
        title="Person age",
        description="This is the person age"
        )
):
    return {name: age}

# Validations: Path Parameters

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=18,
        title="Person id",
        description="This is the person id in db"
        )
):
    return {person_id: "It exists!"}

# Validations: Request body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_201_CREATED)
def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=26,
        title="Person ID",
        description="This is the person ID"
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
