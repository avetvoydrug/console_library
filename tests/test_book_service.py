import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, "..", "."))

sys.path.insert(0, project_root)

import unittest
from unittest.mock import MagicMock

from app.service.book import BookService
from domain.entity.book import Book
from domain.value.book.name import Name
from domain.value.base_value import FrozenSmallText
from domain.exception.value_ex.ex_base_value import FrozenSmallTextLengthError
from infra.repository.book import JSONRepository
from infra.dto.book_dto import BookDTO


class TestBookService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nТесты сервиса запущены")

    @classmethod
    def tearDownClass(cls):
        print("\nТесты сервиса заверщены")
    
    def setUp(self):
        """Метод настройки, выполняемый перед каждым тестом."""
        self.mock_repo = MagicMock(spec=JSONRepository)
        self.service = BookService(self.mock_repo)

    def test_add_book_valid(self):
        """Проверка добавления корректной книги."""
        title="Как достать Володю"
        author=["Гриша","Измайлов"]
        year=1999
        self.service.add_book(title,author,year)
        self.mock_repo().add.assert_called_once()

    def test_add_book_invalid_title(self):
        """Проверка добавления книги с недопустимым названием."""
        res = self.service.add_book("",["GRIR", "SUS"], 555)
        self.assertIsInstance(res, FrozenSmallTextLengthError)

    def test_get_book_existing(self):
        """Проверка получения существующей книги."""
        mock_book = BookDTO
        self.mock_repo().get_by_id.return_value = mock_book 
        retrieved_book = self.service.get_by_id("some_id")
        self.assertEqual(retrieved_book, mock_book)
        self.mock_repo().get_by_id.assert_called_once_with("some_id")

    def test_get_book_non_existing(self):
        """Проверка получения несуществующей книги."""
        self.mock_repo().get_by_id.return_value = None
        retrieved_book = self.service.get_by_id("non_existing_id")
        self.assertIsNone(retrieved_book)
        self.mock_repo().get_by_id.assert_called_once_with("non_existing_id")

    def test_get_all(self):
        """Проверка вызова метода репозитория get_all()"""
        self.service.get_all()
        self.mock_repo().get_all.assert_called_once()

    def test_update_book(self):
        """Проверка вызова метода репозитория get_all()"""
        self.service.update_book("id","new_status")
        self.mock_repo().update.assert_called_once_with("id","new_status")

    def test_delete_book(self):
        """Проверка вызова метода репозитория get_all()"""
        self.service.delete_book("id")
        self.mock_repo().delete.assert_called_once_with("id")
    
    def test_search_by_title_year_author_witout_args(self):
        """Проверка вызова поиска без аргументов"""
        self.service.search()
        self.mock_repo().search_by_title_author_year.assert_called_once_with(None,None,None)



if __name__ == '__main__':
    unittest.main()