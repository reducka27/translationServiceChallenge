from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient


class _AppState:
    _instance: Optional["_AppState"] = None
    mongo_db = None

    def init(self) -> None:
        pass


def get_state() -> "_AppState":
    if _AppState._instance is None:
        _AppState._instance = _AppState()
        _AppState._instance.init()
    return _AppState._instance


def get_db():
    state = get_state()
    if state.mongo_db is None:
        # Connect to MongoDB
        client = AsyncIOMotorClient("mongodb://mongo/")
        state.mongo_db = client["word_definitions"]
    return state.mongo_db


def close_mongo_db(db) -> None:
    if db is None:
        return
    try:
        db.client.close()
    except Exception:
        print("Unknown error attempting to close mongo database client")
        return


def close_db() -> None:
    state = get_state()
    if state.mongo_db is not None:
        close_mongo_db(state.mongo_db)
