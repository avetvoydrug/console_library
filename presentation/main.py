import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, "..", "."))

sys.path.insert(0, project_root)

from typing import List, Optional
from app.service.book import BookService, JSONRepository


def clear_screen():
    """Очищает экран консоли."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Отображает главное меню."""
    clear_screen()
    print("Меню:")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Найти книгу по ID")
    print("4. Вывести все книги")
    print("5. Обновить статус книги")
    print("6. Поиск книг по названию, автору и году издания")
    print("7. Выход")


def get_user_input(prompt: str) -> Optional[str]:
    """Получает ввод пользователя с обработкой ошибок."""
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input.strip()
        else:
            if "или оставьте пустым" in prompt:
                return None
            print("Ввод не может быть пустым. Попробуйте снова.")

def get_int_input(prompt: str) -> Optional[int]:
    while True:
        try:
            user_input = input(prompt)
            if not user_input and "или оставьте пустым" in prompt:
                return None
            user_input = int(user_input)
            return user_input
        except ValueError:
            print("Неверный формат ввода. Пожалуйста, введите целое положительное число.")


def add_book(book_service):
    title = get_user_input("Введите название книги: ")
    while True:
        try:
            author_input = get_user_input("Введите имя, фамилию и отчество автора (через запятую): ").split(",")
            if len(author_input) < 2:
                print("Необходимо указать минимум имя и фамилию автора.")
                continue  

            if len(author_input) > 3:
                print("Все данные после третьей запятой будут потеряны")
                answer = get_user_input("Хотите ввести заново? (да/нет): ")
                if answer.lower() in ["да", "yes"]:
                    continue  
            author = [a.strip() for a in author_input[:3]]
            print(author)  
            break
        except Exception as e:
            print(f"Ошибка: {e}")
    year = get_int_input("Введите год выпуска: ")

    result = book_service.add_book(title, author, year)
    if isinstance(result, Exception):
        print(f"Ошибка при добавлении книги: {result}")
    else:
        print("Книга успешно добавлена!")

def main():
    book_rep = JSONRepository
    book_service = BookService(book_rep)


    while True:
        display_menu()
        choice = get_user_input("Выберите пункт меню: ")

        try:
            if choice == "1":
                add_book(book_service)
            elif choice == "2":
                book_id = get_user_input("Введите ID книги для удаления: ")
                result = book_service.delete_book(book_id)
                if isinstance(result, Exception):
                    print(f"Ошибка при удалении книги: {result}")
                else:
                    print(result)
            elif choice == "3":
                book_id = get_user_input("Введите ID книги: ")
                result = book_service.get_by_id(book_id)
                if isinstance(result, Exception):
                    print(f"Ошибка сервиса: {result}")
                elif result is None:
                    print("Книги с таким ID не существует")
                else:
                    print(result)
            elif choice == "4":
                books = book_service.get_all()
                if isinstance(books, Exception):
                    print(f"Ошибка сервиса: {result}")
                else:
                    for book in books:
                        print(book)
            elif choice == "5":
                book_id = get_user_input("Введите ID книги для обновления статуса: ")
                new_status = get_user_input("Введите новый статус(выдана/в наличии): ")
                result = book_service.update_book(book_id, new_status)
                if isinstance(result, Exception):
                    print(f"Ошибка при обновлении статуса: {result}")
                else:
                    print("Статус обновлён")
            elif choice == "6":
                print("\n\nЕсли не найдётся ни одной книги вернуться все, что есть в библиотеке")
                print("Если будет несколько совпадений вернуться все совпавшие\n")
                title = get_user_input("Введите название полностью или частично или оставьте пустым: ")
                author = get_user_input("Введите ФИО (через пробел или оставьте пустым): ")
                year = get_int_input("Введите год издания или оставьте пустым: ")
                result = book_service.search(title, author, year)
                if isinstance(result, Exception):
                    print(f"Ошибка при обновлении статуса: {result}")
                if isinstance(result, List):
                    for book in result:
                        print(book)
                else:
                    print(result)

            elif choice == "7":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
        input("Нажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()