# Hello World in FastAPI

---

> ***v1.1*** - This is an initial project in a learning path, it includes topics as:

*Some features*

- The models, views and forms of this project are in the same file.

- The project don't use a user interface other than documentation views, such as swagger or redoc.

- It uses some very basic management of multimedia files.

- It uses base authentication.

- The project does not use any database.

- Validations: Query and Path Parameters.

- Some about cookies.

## Versions

```
fastapi 0.79.0
uvicorn 0.18.2
python-multipart 0.0.5
email-validator 1.2.1

OAS 3.0
```

You can see complete requirements in [requirements.txt](requirements.txt)

## How to run locally this app?

```
uvicorn main:app --reload
```

## Interactive documentation

**FastAPI** documents the code directly and automatically and it's based on Swagger.

<center>

| FastAPI |
| --- |
| Swagger |
| OpenAPI |

</center>

### How to show Swagger documentation?

```
http://127.0.0.1:8000/docs
```

### How to show ReDoc documentation?

```
http://127.0.0.1:8000/redoc
```

# Bibliography

- [Swagger UI](https://swagger.io/tools/swagger-ui/)
