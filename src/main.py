from fastapi import FastAPI

from routers import words
from depends import close_db

app = FastAPI()

app.include_router(words.router)


@app.on_event("shutdown")
def shutdown_event() -> None:
    print("Closing database connections in shutdown hook")
    close_db()
