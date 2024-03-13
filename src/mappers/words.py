from models.word_item import WordItem
from models.paginations import Pagination, Page
from models.deleted_result import DeletedResult
from models.word_item import build_word_item_from_google_translate
from depends import get_db
from googletrans import Translator

translator = Translator()


async def get_by_name(word: str, db=None) -> WordItem:
    if db is None:
        db = get_db()

    word_data = await db.words.find_one({"word": word}, {"_id": 0})
    if not word_data:
        response = translator.translate(word, src="en", dest="es")
        word_data = build_word_item_from_google_translate(word, response)
        await db.words.insert_one(word_data.dict())
    else:
        word_data = WordItem(**word_data)

    return word_data


async def find_all(
    pagination: Pagination,
    include_definitions: bool,
    include_synonyms: bool,
    include_translations: bool,
    db=None,
) -> Page[WordItem]:
    if db is None:
        db = get_db()

    query = {}
    if pagination.filter:
        query = {"word": {"$regex": f".*{pagination.filter}.*", "$options": "i"}}
    show_attributes = {}
    if include_definitions:
        show_attributes["definitions"] = 1
    if include_synonyms:
        show_attributes["synonyms"] = 1
    if include_translations:
        show_attributes["translations"] = 1

    cursor = (
        db.words.find(query, {"_id": 0, "word": 1, **show_attributes})
        .skip(pagination.skip)
        .limit(pagination.limit)
    )
    if pagination.sort:
        cursor.sort(pagination.sort)
    words = await cursor.to_list(length=pagination.limit)
    total = await db.words.count_documents(query)
    page = Page(count=len(words), total=total, results=words)
    return page


async def delete(word: str, db=None) -> DeletedResult:
    if db is None:
        db = get_db()

    result = await db.words.delete_one({"word": word})
    return {"deleted": result.deleted_count}
