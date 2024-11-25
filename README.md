# Консольное приложение для управления книгами, написана по принципу DDD

Это консольное приложение позволяет управлять базой данных книг, используя простой текстовый интерфейс.  Приложение позволяет добавлять, удалять, искать и обновлять информацию о книгах.  Данные хранятся в файле `db.json`.('db.json' не много заполнена, если уалить создастся новый путой файл) Написаны и пройдены тесты для book_repository и book_service

## Функциональность

* **Добавление книги:**  Введите название книги, имя, фамилию и отчество автора (через запятую), и год выпуска. (*отчество не обязательно, другие поля оставить пустыми не получится)
* **Удаление книги:** Введите ID книги для удаления. Приложение проверит наличие книги перед удалением.
* **Поиск книги по ID:** Введите ID книги, чтобы получить подробную информацию о ней.
* **Просмотр всех книг:** Выведите список всех книг в базе данных.
* **Обновление статуса книги:**  Введите ID книги и новый статус.
* **Поиск книг:** Выполните поиск книг по названию, автору или году выпуска.  Вы можете комбинировать критерии поиска (*названию и автору не обязательно точное совпадение)

## Требования

* Python 3.7+

# Запуск
- клонируйте репозиторий
- перейдите в директорию с проектом
- запустите тесты
```bash
python<ваш_пайтон> -m unittest discover tests
```
- запустите приложение
```bash
python<ваш_пайтон> presentation/main.py
```
# Структура
- library/
- ├── app/                 # Бизнес-логика
- │   └── service/
- │       └── book.py      # BookService
- │
- ├── infra/               # Инфраструктура
- │   ├──dto
- │   │  └──book_dto.py    # data transfer object для Book
- │   └──repository
- │      └──book.py        # работа с БД JSONRepository
- │
- ├── domain/              # Доменная область
- │   ├──entity            # Сущности
- │   │  └──book.py        
- │   ├──exception         # Исключения для сущностей и объект-значений
- │   │  ├──entity_ex     
- │   │  └──value_ex
- │   └──value             # Объекты значений
- ├── presentation/
- │   └──main.py           # Презентационный слой (консольный интерфейс)
- │
- └──tests/                # тесты
-    ├──test_book_repository.py     # интеграционные
-    └──test_book_service.py        # модульные
