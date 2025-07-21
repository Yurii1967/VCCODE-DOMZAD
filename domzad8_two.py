


import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    pattern = r'(?:^|\s)(\d+(?:\.\d+)?)(?=\s|$)'
    for match in re.findall(pattern, text):
        yield float(match)

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    return sum(func(text))

text = "Доходи за місяць: 100.50 200.75 300"
result = sum_profit(text, generator_numbers)
print(result)  # Виведе: 601.25
