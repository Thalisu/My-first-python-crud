from exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)
from datetime import datetime
from typing import Dict


def data_processing(data: Dict[str, str | int]) -> list[bool, Exception]:
    TITLES = data.get("titles")
    if TITLES < 0:
        raise NegativeTitlesError("titles cannot be negative")

    FIRST_CUP = int(data.get("first_cup")[:4])
    if FIRST_CUP < 1930 or (FIRST_CUP - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")

    CURRENT_YEAR = datetime.now().year

    if TITLES > (CURRENT_YEAR - FIRST_CUP) // 4:
        raise ImpossibleTitlesError(
            "impossible to have more titles than disputed cups"
        )
