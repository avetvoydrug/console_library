import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, "..", "."))

sys.path.insert(0, project_root)

import unittest
from unittest.mock import MagicMock
from pathlib import Path

from domain.entity.book import Book
from domain.value.book.name import Name
from domain.value.base_value import FrozenSmallText
from domain.exception.value_ex.ex_base_value import FrozenSmallTextLengthError
from infra.repository.book import JSONRepository
from infra.dto.book_dto import BookDTO


class TestBookRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Метод настройки, выполняемый один раз перед тестированием."""
        print("Тесты репозитория запущены")
        cls.test_repo = JSONRepository("test_db.json")
        cls.valid_book = Book(
            title=FrozenSmallText("RUSSIA"),
            year=100,
            author=Name(
                first_name=FrozenSmallText("vanya"),
                last_name=FrozenSmallText("vanya")),
            )

    @classmethod
    def tearDownClass(cls):
        """Удаление тестовую БД"""
        try:
            print("\nТесты репозитория завершены")
            Path("test_db.json").unlink()
            print("Тестовая бд удалена")
        except FileNotFoundError:
            pass
    
    @staticmethod
    def make_valid_book(
        title:str, 
        first_name:str, 
        last_name:str, 
        year:int)->Book:
        """
        Создаёт новую валидную книгу
        """
        one_more_valid_book = Book(
            title=FrozenSmallText(title),
            year=year,
            author=Name(
                first_name=FrozenSmallText(first_name),
                last_name=FrozenSmallText(last_name)),
            )
        return one_more_valid_book

    def test_add_book_valid(self):
        """Проверка добавления корректной книги."""
        id = self.valid_book.id
        self.test_repo.add(self.valid_book)
        input("test_db создана. Нажмите Enter, чтобы продолжить")
        result = self.test_repo.get_by_id(id)
        self.assertIsInstance(result, BookDTO)
    
    def test_get_all(self):
        """
        Проверка добавления корректной книги.
        На момент выполнения в test_db после первого теста должна
        лежать одна книга
        """
        res = self.test_repo.get_all()
        self.assertEqual(1,len(res))

    def test_update_with_wrong_status(self):
        """
        Проверка отрабатывания исключения при неверном статусе
        """
        with self.assertRaises(ValueError):
            id = self.valid_book.id
            self.test_repo.update(id, "Hmmmmm")
    
    def test_update_with_valid_status(self):
        """
        Проверка обновления при валидном статусе
        """
        id = self.valid_book.id
        before = self.test_repo.get_by_id(id)
        self.test_repo.update(id, "выдана")
        after = self.test_repo.get_by_id(id)
        self.assertNotEqual(before.status, after.status)

    def test_search_by_author_valid(self):
        """
        Проверка при валидном поиске по автору
        *Автора необязательно вводить полностью, в результирующий
            набор добавляются все варианты, у которых есть совпадение
            а-ля if a in bi: res.append(bi)
        """
        # Добавим ещё книгу(во всех тестахпоиска логика похожая)
        one_more_valid_book = self.make_valid_book(
            title="NOTRUSSIA",
            first_name="kalyvan",
            last_name="kalyvan",
            year=500
        )
        self.test_repo.add(one_more_valid_book)
        res_search = self.test_repo.search_by_title_author_year(author="kaly")
        res_all = self.test_repo.get_all()
        # До этого теста в test_db уже была одна запись + 1 уникальную книгу
        # только что добавили => длина рез. списка не должна быть равна кол-ву всех книг
        self.assertNotEqual(len(res_search), len(res_all))
        # Смотрим совпадает ли год выпуска книги найденной с запрошенной
        self.assertEqual(res_search[0].year, one_more_valid_book.year)
    
    def test_search_by_year_valid(self):
        """
        Проверка при валидном поиске по году
        """
        one_more_valid_book = self.make_valid_book(
            title="NOTRUSSIA",
            first_name="kalyvan",
            last_name="kalyvan",
            year=666
        )
        self.test_repo.add(one_more_valid_book)
        res_search = self.test_repo.search_by_title_author_year(year=666)
        res_all = self.test_repo.get_all()
        self.assertNotEqual(len(res_search), len(res_all))
        self.assertEqual(res_search[0].year, one_more_valid_book.year)

    def test_search_by_part_title(self):
        """
        Проверка при валидном поиске по названию
        *Название необязательно вводить полностью, в результирующий
            набор добавляются все варианты, у которых есть совпадение
        """
        one_more_valid_book = self.make_valid_book(
            title="Анекдоты",
            first_name="me",
            last_name="me",
            year=666
        )
        self.test_repo.add(one_more_valid_book)
        res_search = self.test_repo.search_by_title_author_year(title="доты")
        res_all = self.test_repo.get_all()
        self.assertNotEqual(len(res_search), len(res_all))
        self.assertEqual(res_search[0].year, one_more_valid_book.year)
    
    def test_delete_with_existing_id(self):
        """
        Проверка отработки при удалении существующей книги
        """
        book = self.make_valid_book(
            title="any",
            first_name="any",
            last_name="any",
            year=123)
        # Добавляем новую книгу
        self.test_repo.add(book)
        # Проверяем, что она есть
        id = book.id
        res = self.test_repo.get_by_id(id)
        if res is not None:
            res = self.test_repo.delete(id)
            self.assertEqual(res, "Книга успешно удалена!")
        else:
            self.assertEqual("Обвал теста","")
    
    def test_delete_with_wrong_id(self):
        """
        Проверка отработки при удалении не существующей книги
        """
        res = self.test_repo.delete("dgskds")
        self.assertEqual(res, "Книга не существует")


if __name__ == '__main__':
    unittest.main()