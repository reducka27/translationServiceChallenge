from models.word_item import WordItem
from models.paginations import Pagination
from models.paginations import Page
from models.deleted_result import DeletedResult
import services.words as word_item_service


async def get_by_name(word: str) -> WordItem:
    return await word_item_service.get_by_name(word)


async def find_all(
    pagination: Pagination,
    include_definitions: bool,
    include_synonyms: bool,
    include_translations: bool,
) -> Page[WordItem]:
    return await word_item_service.find_all(
        pagination, include_definitions, include_synonyms, include_translations
    )


async def delete(word: str) -> DeletedResult:
    return await word_item_service.delete(word)
