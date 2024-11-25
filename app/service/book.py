from typing import List, Optional

from infra.repository.book import JSONRepository
from infra.dto.book_dto import BookDTO
from domain.entity.book import Book, Name, FrozenSmallText


class BookService:
    def __init__(self, book_rep: type[JSONRepository]):
        """
        Инициализация репозитория и файла с бд
        """
        self.book_rep: JSONRepository = book_rep("db.json")

    def add_book(self, title: str, author: List[str], year: int):
        """
        Добавление новой книги        
        """
        try:

            middle_name = FrozenSmallText(author[2]) if len(author) == 3 else None
            book = Book(
                title=FrozenSmallText(title), 
                author=Name(
                    first_name=FrozenSmallText(author[0]),
                    last_name=FrozenSmallText(author[1]),
                    middle_name=middle_name), 
                year=year)
            self.book_rep.add(book)
        except Exception as e:
            return e
        
    def delete_book(self, id: str):
        """
        Удаление книги по id
        """
        try:
            res = self.book_rep.delete(id)
            return res
        except Exception as e:
            return e
    
    def get_by_id(self, id: str)->Optional[BookDTO]:
        """
        Получение книги по id
        """
        res = self.book_rep.get_by_id(id)
        return res
    
    def get_all(self)->List[BookDTO]:
        """
        Получение всех книг из БД
        """
        res = self.book_rep.get_all()
        return res

    def update_book(self, id: str, status: str)->None:
        """
        Обновление статуса книги
        """
        self.book_rep.update(id, status)
    
    def search(
        self, 
        title: Optional[str] = None, 
        author: Optional[str] = None, 
        year: Optional[int] = None)->List[BookDTO]:
        """
        Возвращает или:
            - список книг по входным данным
            - список всех книг
        """
        res = self.book_rep.search_by_title_author_year(title, author, year)
        return res
