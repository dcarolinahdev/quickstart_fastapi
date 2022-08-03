# Python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field, EmailStr
# FastAPI
from fastapi import FastAPI, status, HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="matt2022g"
    )
    message: str = Field(default="Login Succesfully!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=['Index']
)
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons']
)
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons']
)
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

persons = [1, 2, 3, 4, 5]

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons']
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=18,
        title="Person id",
        description="This is the person id in db"
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validations: Request body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_201_CREATED,
    tags=['Persons']
)
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

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Auth']
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Forms']
)
def contact(
    first_name: str = Form(
        ...,
        min_length=1,
        max_length=20
    ),
    last_name: str = Form(
        ...,
        min_length=1,
        max_length=20
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# files

@app.post(
    path='/post-image',
    tags=['Forms']
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
