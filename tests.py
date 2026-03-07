import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    # Тест на проверку максимальной длины названия книги (40 символов)
    def test_add_new_book_name_length_40_symbols(self):
        collector = BooksCollector()
        name = 'a' * 40
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    # Тест на проверку, что книга с названием длиннее 40 символов не добавляется
    def test_add_new_book_name_length_more_40_symbols_not_added(self):
        collector = BooksCollector()
        name = 'a' * 41
        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == 0

    # Тест на проверку, что нельзя добавить одну и ту же книгу дважды
    def test_add_new_same_book_twice_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_new_book('Книга')
        assert len(collector.get_books_genre()) == 1

    # Тест на проверку, что у новой книги нет жанра
    def test_add_new_book_has_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        assert collector.get_book_genre('Книга') == ''

    # Тест на установку жанра книге
    def test_set_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_book_genre('Книга') == 'Фантастика'

    # Параметризованный тест на проверку, что нельзя установить несуществующий жанр
    @pytest.mark.parametrize('genre', ['Роман', 'Поэма', 'Сказка'])
    def test_set_book_genre_with_invalid_genre_not_set(self, genre):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_book_genre('Книга') == ''

    # Тест на получение списка книг определенного жанра
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

    # Тест на получение списка книг для детей (без возрастного рейтинга)
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

    # Тест на добавление книги в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        assert 'Книга' in collector.get_list_of_favorites_books()

    # Тест на проверку, что нельзя добавить в избранное несуществующую книгу
    def test_add_nonexistent_book_in_favorites_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    # Тест на проверку, что нельзя добавить одну книгу в избранное дважды
    def test_add_same_book_in_favorites_twice_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.get_list_of_favorites_books()) == 1

    # Тест на удаление книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()

    # Тест на удаление несуществующей книги из избранного (не должно быть ошибки)
    def test_delete_nonexistent_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        initial_favorites = collector.get_list_of_favorites_books().copy()
        collector.delete_book_from_favorites('Несуществующая книга')
        assert collector.get_list_of_favorites_books() == initial_favorites