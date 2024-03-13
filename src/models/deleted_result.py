from pydantic import BaseModel


class DeletedResult(BaseModel):
    deleted: int
