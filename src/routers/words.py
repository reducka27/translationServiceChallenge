from typing import List, Optional

from fastapi import APIRouter

from models.word_item import WordItem
from models.paginations import Page
from models.paginations import create_pagination
from models.deleted_result import DeletedResult
import handlers.words as word_item_handler

router = APIRouter()


@router.get("/word/{word}", response_model=WordItem)
async def get_word(word: str) -> WordItem:
    res = await word_item_handler.get_by_name(word)
    return res


@router.get("/words", response_model=Page[WordItem])
async def get_words(
    skip: int = 0,
    limit: int = 10,
    word_filter: str = None,
    sort: str = None,
    include_definitions: bool = False,
    include_synonyms: bool = False,
    include_translations: bool = False,
) -> Page[WordItem]:
    pagination = create_pagination(
        filter=word_filter, sort=sort, limit=limit, skip=skip
    )

    res = await word_item_handler.find_all(
        pagination, include_definitions, include_synonyms, include_translations
    )
    return res


@router.delete("/word/{word}", response_model=DeletedResult)
async def delete_word(word: str) -> DeletedResult:
    res = await word_item_handler.delete(word)
    return res
