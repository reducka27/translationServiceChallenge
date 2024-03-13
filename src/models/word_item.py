from typing import Union
from pydantic import BaseModel
from utils.flatten_list import flatten_concatenation
from googletrans.models import Translated


class WordItem(BaseModel):
    word: str
    translations: list
    definitions: Union[list, None]
    synonyms: Union[list, None]
    examples: Union[list, None]


def build_word_item_from_google_translate(word: str, glr: Translated) -> WordItem:
    translations = [
        translation[0]
        for translation in glr.extra_data.get("translation")
        if translation and translation[0]
    ]
    examples = [example[0] for example in glr.extra_data.get("examples")[0] if example]
    synonyms = flatten_concatenation(
        [
            synonym[1][0][0]
            for synonym in glr.extra_data.get("synonyms")
            if synonym and synonym[1][0]
        ]
    )
    definitions = glr.extra_data.get("definitions")
    word_item = WordItem(
        word=word,
        translations=translations,
        examples=examples,
        synonyms=synonyms,
        definitions=definitions,
    )
    return word_item
