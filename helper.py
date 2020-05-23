from typing import Iterator

def char_range(start: str, end: str) -> Iterator[str]:
    for i in range(ord(start), ord(end) + 1):
        yield chr(i)
