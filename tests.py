import pytest
from main import BooksCollector

class TestBooksCollector:

    # Проверяет, что метод add_new_book добавляет книгу в словарь books_genre
    # Ожидаемый результат: после добавления двух книг размер словаря равен 2
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Проверяет граничное значение длины названия книги (максимум 40 символов)
    # Ожидаемый результат: книга с названием из 40 символов успешно добавляется
    def test_add_new_book_name_length_40_symbols(self):
        collector = BooksCollector()
        name = 'a' * 40
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    # Проверяет, что книга с названием длиннее 40 символов не добавляется
    # Ожидаемый результат: словарь книг остается пустым
    def test_add_new_book_name_length_more_40_symbols_not_added(self):
        collector = BooksCollector()
        name = 'a' * 41
        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == 0

    # Проверяет, что нельзя добавить одну и ту же книгу дважды
    # Ожидаемый результат: после двух попыток добавить одну книгу, в словаре только одна запись
    def test_add_new_same_book_twice_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_new_book('Книга')
        assert len(collector.get_books_genre()) == 1

    # Проверяет, что у новой книги жанр не установлен (пустая строка)
    # Ожидаемый результат: get_book_genre возвращает пустую строку для новой книги
    def test_add_new_book_has_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        assert collector.get_book_genre('Книга') == ''

    # Проверяет успешную установку жанра для существующей книги
    # Ожидаемый результат: get_book_genre возвращает установленный жанр
    def test_set_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_book_genre('Книга') == 'Фантастика'

    # Параметризованный тест проверяет, что нельзя установить несуществующий жанр
    # Ожидаемый результат: жанр книги остается пустой строкой
    @pytest.mark.parametrize('genre', ['Роман', 'Поэма', 'Сказка'])
    def test_set_book_genre_with_invalid_genre_not_set(self, genre):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_book_genre('Книга') == ''

    # Проверяет получение списка книг определенного жанра
    # Ожидаемый результат: возвращаются только книги с указанным жанром
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_new_book('Книга 3')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Фантастика')
        collector.set_book_genre('Книга 3', 'Ужасы')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == 2
        assert 'Книга 1' in fantasy_books
        assert 'Книга 2' in fantasy_books
        assert 'Книга 3' not in fantasy_books

    # Проверяет фильтрацию книг для детей (исключает жанры с возрастным рейтингом)
    # Ожидаемый результат: в списке для детей нет книг жанров Ужасы и Детективы
    def test_get_books_for_children_excludes_age_rated_books(self):
        collector = BooksCollector()
        collector.add_new_book('Книга для детей')
        collector.add_new_book('Страшная книга')
        collector.add_new_book('Детектив')
        collector.set_book_genre('Книга для детей', 'Мультфильмы')
        collector.set_book_genre('Страшная книга', 'Ужасы')
        collector.set_book_genre('Детектив', 'Детективы')

        children_books = collector.get_books_for_children()
        assert 'Книга для детей' in children_books
        assert 'Страшная книга' not in children_books
        assert 'Детектив' not in children_books

    # Проверяет добавление книги в избранное
    # Ожидаемый результат: книга появляется в списке избранного
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        assert 'Книга' in collector.get_list_of_favorites_books()

    # Проверяет, что нельзя добавить несуществующую книгу в избранное
    # Ожидаемый результат: список избранного остается пустым
    def test_add_nonexistent_book_in_favorites_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    # Проверяет, что нельзя добавить одну книгу в избранное дважды
    # Ожидаемый результат: в избранном только одна копия книги
    def test_add_same_book_in_favorites_twice_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.get_list_of_favorites_books()) == 1

    # Проверяет удаление книги из избранного
    # Ожидаемый результат: книга пропадает из списка избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()

    # Проверяет удаление несуществующей книги из избранного (не должно вызывать ошибку)
    # Ожидаемый результат: список избранного не изменяется
    def test_delete_nonexistent_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        initial_favorites = collector.get_list_of_favorites_books().copy()
        collector.delete_book_from_favorites('Несуществующая книга')
        assert collector.get_list_of_favorites_books() == initial_favorites

    # НОВЫЕ ТЕСТЫ для прямого тестирования методов

    # Проверяет, что метод get_books_genre возвращает словарь с правильными данными
    # Ожидаемый результат: возвращается словарь, содержащий все книги с их жанрами
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        
        books_genre = collector.get_books_genre()
        
        assert isinstance(books_genre, dict)
        assert len(books_genre) == 2
        assert books_genre['Книга 1'] == 'Фантастика'
        assert books_genre['Книга 2'] == ''

    # Проверяет, что метод get_book_genre возвращает правильный жанр для существующей книги
    # Ожидаемый результат: возвращается жанр, который был установлен для книги
    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Детективы')
        
        genre = collector.get_book_genre('Книга')
        
        assert genre == 'Детективы'

    # Проверяет, что метод get_book_genre возвращает None для несуществующей книги
    # Ожидаемый результат: при запросе жанра несуществующей книги возвращается None
    def test_get_book_genre_returns_none_for_nonexistent_book(self):
        collector = BooksCollector()
        
        genre = collector.get_book_genre('Несуществующая книга')
        
        assert genre is None

    # Проверяет, что метод get_list_of_favorites_books возвращает список избранных книг
    # Ожидаемый результат: возвращается список, содержащий только книги из избранного
    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')
        
        favorites = collector.get_list_of_favorites_books()
        
        assert isinstance(favorites, list)
        assert len(favorites) == 1
        assert 'Книга 1' in favorites
        assert 'Книга 2' not in favorites

    # Проверяет, что при создании коллектора список избранного пуст
    # Ожидаемый результат: get_list_of_favorites_books возвращает пустой список
    def test_get_list_of_favorites_books_returns_empty_list_initially(self):
        collector = BooksCollector()
        
        favorites = collector.get_list_of_favorites_books()
        
        assert isinstance(favorites, list)
        assert len(favorites) == 0