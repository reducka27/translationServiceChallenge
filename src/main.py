from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from routers import words
from depends import close_db

app = FastAPI()

app.include_router(words.router)


@app.on_event("shutdown")
def shutdown_event() -> None:
    print("Closing database connections in shutdown hook")
    close_db()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Translation Service Challenge",
        version="0.0.1",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
