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
    tags=['Persons'],
    summary="Create person in the app"
)
def create_person(person: Person = Body(...)):
    """
    ***Create person***

    This path operation creates a person in the app and save the information in database.

    Parameters:
    - Request body parameter:
        - **person: Person**:
            A person model with firstname, lastname, age, hair color and marital status.

    Returns:
    - **person model**:
        A person model with firstname, lastname, age, hair color and marital status.
    """
    return person

# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary="Show person detail info in the app",
    deprecated=True
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
    """
    ***Show person***

    This path operation show the main detail of a person .

    Parameters:
    - Request body parameter:
        - **name: str**:
            A name for person.
        - **age: int**:
            Age for person.

    Returns:
    - **python dict**:
        A python dict with firstname and lastname as key and age as value.
    """
    return {name: age}

# Validations: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary="Show if person exists in the app"
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
    """
    ***Show if person exists in db***

    This path operation show if person exisst.

    Parameters:
    - Request body parameter:
        - **person_id: int**:
            Person identification in database.

    Returns:
    - **python dict**:
        A python dict with identification in database as key and message as value.
    """
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
    tags=['Persons'],
    summary="Update a person in the app"
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
    """
    ***Updates a person in db***

    This path operation updates a person data.

    Parameters:
    - Request body parameter:
        - **person_id: int**:
            Person identification in database.
        - **person: Person**:
            Person data as json info.
        - **location: Location**:
            Location data as json info.

    Returns:
    - **python dict**:
        A person as a dict.
    """
    results = person.dict()
    results.update(location.dict())
    return results

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Auth'],
    summary="Login in the app"
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    ***Login user in app***

    This path operation login an user in app.

    Parameters:
    - Request body parameter:
        - **username: str**:
            Person username in db.
        - **password: str**:
            Person password in db.

    Returns:
    - **redirect to viewt**:
        Redirect to future view
    """
    return LoginOut(username=username)

# Cookies and Headers parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Forms'],
    summary="Contact form"
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
    """
    ***Contact form***

    This path operation send a message in contact form.

    Parameters:
    - Request body parameter:
        - **firstname: str**:
            Person firstname.
        - **lastname: str**:
            Person dlastname.
        - **email: EmailStr**:
            User email.
        - **message: str**:
            Message to send.
        - **user_agent: str**:
            User agent from header.
        - **ads: str**:
            Ads from cookies.

    Returns:
    - **user_agent**:
        User agent.
    """
    return user_agent

# files

@app.post(
    path='/post-image',
    tags=['Forms'],
    summary="Send image in post"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    ***Post an image***

    This path operation post an image.

    Parameters:
    - Request body parameter:
        - **image: file**:
            Image file.

    Returns:
    - **python dict**:
        A dict with filename, format and size in kb.
    """
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
