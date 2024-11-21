from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BookDTO:
    id: str
    title: Dict[str, str]
    year: int
    author: Dict[str, Dict[str, str]]
    status: str

    def __str__(self):
        middle_name = self.author["middle_name"]["text"] + " " if self.author["middle_name"] else " "
        author = self.author["first_name"]["text"] + " " +\
            middle_name + self.author["last_name"]["text"]
        return f"ID '{self.id}'\nНазвание '{self.title["text"]}'\n"\
            f"Год выпуска {self.year}\nАвтор '{author}'\nСтатус '{self.status}'\n"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)