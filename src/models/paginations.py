from typing import List, Optional, Tuple, TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel


PageResultT = TypeVar("PageResultT")


class Pagination(BaseModel):
    filter: Optional[str]
    sort: List[Tuple[str, int]] = []
    limit: int
    skip: int = 0


class Page(GenericModel, Generic[PageResultT]):
    count: Optional[int]
    total: int
    results: List[PageResultT]


def create_pagination(
    filter: Optional[str],
    sort: Optional[str],
    limit: Optional[int],
    skip: Optional[int],
) -> Pagination:
    if skip is None:
        skip = 0
    if limit is None:
        limit = 0

    if sort:
        sort_ = sort.split(",")
    else:
        sort_ = []
    final_sort = []
    for s in sort_:
        vals = s.split(":")
        if len(vals) != 2:
            raise Exception("Invalid Sort Parameters")
        if vals[1] in ("asc", "1"):
            final_sort.append((vals[0], 1))
        elif vals[1] in ("desc", "-1"):
            final_sort.append((vals[0], -1))
        else:
            raise Exception("Invalid Sort parameters")

    _skip = skip

    pagination = Pagination(filter=filter, sort=final_sort, limit=limit, skip=_skip)

    return pagination
