import json
import uuid
from dataclasses import asdict, dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

#domain
from domain.entity.book import Book
from infra.repository.base import BaseRepository
from infra.dto.book_dto import BookDTO

class JSONRepository(BaseRepository):
    """
    Репозиторий для работы с книгами        
    """
    def __init__(self, filename: str):
        self.filename = filename
        Path(self.filename).touch() #Создать пустой файл, если его не существует
    
    def _ensure_file_exists(self):
        """Создает пустой, валидный JSON-файл, если он не существует."""
        if not Path(self.filename).exists():
            self._save_data({"books": []})

    def _load_data(self) -> Dict[str, Any]:
        """
        Загружает данные из БД
        """
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._ensure_file_exists()
            return {"books": []}

    def _save_data(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные в БД
        """
        with open(self.filename, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_all(self) -> List[BookDTO]:
        """
        Получение всех книг из БД
        """
        data = self._load_data()
        return [BookDTO.from_dict(item) for item in data["books"]]

    def get_by_id(self, book_id: str) -> Optional[BookDTO]:
        """
        Получение книги по id
        """
        data = self._load_data()
        for item in data["books"]:
            if item["id"] == book_id:
                return BookDTO.from_dict(item)
        return None

    def add(self, book: Book) -> None:
        """
        Добавление новой книги        
        """
        data = self._load_data()
        data["books"].append(book.to_dict())
        self._save_data(data)

    def update(self, id: str, status: str) -> None:
        """
        Обновление статуса книги
        """
        if status not in ("в наличии", "выдана"):
            raise ValueError(f"статус должен быть в наличии или выдана\n"\
                f"Вы ввели '{status}'")
        data = self._load_data()
        for i, item in enumerate(data["books"]):
            if item["id"] == id:
                data["books"][i]["status"] = status
                self._save_data(data)
                return
        raise ValueError(f"Книга с ID '{id}' не найдена")

    def delete(self, book_id: str) -> str:
        """
        Удаление книги по id
        """
        data = self._load_data()
        book_index = next((i for i, item in enumerate(data["books"]) if item["id"] == book_id), None)

        if book_index is not None:
            del data["books"][book_index]
            self._save_data(data)
            return "Книга успешно удалена!"
        else:
            return "Книга не существует"

    def search_by_title_author_year(
        self, 
        title: Optional[str] = None, 
        author: Optional[str] = None, 
        year: Optional[int] = None
        ) -> List[BookDTO]:
        """Возвращает или:
            - список книг по входным данным
            - список всех книг
        """
        if not (title or year or author):
            return self.get_all()
        data = self._load_data()
        results = []
        for book_data in data["books"]:
            book = BookDTO.from_dict(book_data)
            match_title = not title or title.lower() in book.title["text"].lower()
            match_year = not year or book.year == year
            first_name = book.author.get("first_name", {}).get("text", "")
            last_name = book.author.get("last_name", {}).get("text", "")
            middle_name = book.author.get("middle_name", {})
            author_name = f"{first_name} {last_name}"
            if middle_name:
                middle_name = middle_name.get("text", "")
                author_name = f"{first_name} {middle_name} {last_name}"
            math_author = not author or author.lower() in author_name.lower()
            if match_title and match_year and math_author:
                results.append(book)
            
        if results:
            return results
        return self.get_all()

