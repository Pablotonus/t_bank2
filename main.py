import json
import os
from collections import Counter

class TLibrary:
    def __init__(self, filepath="library_data.json"):
        self.filepath = filepath
        self.books = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                self.books = []

    def save_data(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def generate_id(self):
        if not self.books:
            return 1
        return max(book.get('id', 0) for book in self.books) + 1

    def add_book(self):
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        genre = input("Жанр: ").strip()
        
        while True:
            year_str = input("Год издания: ").strip()
            if year_str.isdigit():
                year = int(year_str)
                break
            print("Ошибка: год должен быть числом.")
            
        description = input("Краткое описание: ").strip()

        book = {
            "id": self.generate_id(),
            "title": title,
            "author": author,
            "genre": genre,
            "year": year,
            "description": description,
            "is_read": False,
            "is_favorite": False
        }
        self.books.append(book)
        self.save_data()
        print("\nКнига успешно добавлена!")

    def display_books(self, books_to_display=None):
        target_books = books_to_display if books_to_display is not None else self.books
        if not target_books:
            print("\nСписок пуст.")
            return

        for b in target_books:
            status = "Прочитана" if b['is_read'] else "Не прочитана"
            fav = "★" if b['is_favorite'] else "☆"
            print(f"[{b['id']}] {fav} {b['title']} — {b['author']} ({b['year']}) | Жанр: {b['genre']} | Статус: {status}")

    def view_and_filter_books(self):
        print("\n1. Показать все")
        print("2. Сортировка по названию")
        print("3. Сортировка по автору")
        print("4. Сортировка по году")
        print("5. Фильтр по жанру")
        print("6. Фильтр по статусу (прочитана/не прочитана)")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            self.display_books()
        elif choice == '2':
            self.display_books(sorted(self.books, key=lambda x: x['title'].lower()))
        elif choice == '3':
            self.display_books(sorted(self.books, key=lambda x: x['author'].lower()))
        elif choice == '4':
            self.display_books(sorted(self.books, key=lambda x: x['year']))
        elif choice == '5':
            genre = input("Введите жанр: ").strip().lower()
            filtered = [b for b in self.books if b['genre'].lower() == genre]
            self.display_books(filtered)
        elif choice == '6':
            status = input("1 - Прочитана, 2 - Не прочитана: ").strip()
            is_read = status == '1'
            filtered = [b for b in self.books if b['is_read'] == is_read]
            self.display_books(filtered)

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book['id'] == book_id:
                return book
        return None

    def manage_book(self):
        self.display_books()
        try:
            book_id = int(input("\nВведите ID книги для управления: ").strip())
        except ValueError:
            print("Неверный ID.")
            return

        book = self.find_book_by_id(book_id)
        if not book:
            print("Книга не найдена.")
            return

        print(f"\nВыбрана книга: {book['title']}")
        print("1. Изменить статус (прочитана/не прочитана)")
        print("2. Добавить/удалить из избранного")
        print("3. Удалить книгу из библиотеки")
        
        choice = input("Действие: ").strip()
        
        if choice == '1':
            book['is_read'] = not book['is_read']
            status = "Прочитана" if book['is_read'] else "Не прочитана"
            print(f"Статус изменен на: {status}")
        elif choice == '2':
            book['is_favorite'] = not book['is_favorite']
            status = "добавлена в избранное" if book['is_favorite'] else "удалена из избранного"
            print(f"Книга {status}.")
        elif choice == '3':
            self.books.remove(book)
            print("Книга удалена.")
        
        self.save_data()

    def search_books(self):
        query = input("Введите ключевое слово (название, автор или описание): ").strip().lower()
        results = []
        for b in self.books:
            if (query in b['title'].lower() or 
                query in b['author'].lower() or 
                query in b['description'].lower()):
                results.append(b)
        
        print("\nРезультаты поиска:")
        self.display_books(results)

    def show_favorites_and_recommendations(self):
        print("\n--- Избранное ---")
        favorites = [b for b in self.books if b['is_favorite']]
        self.display_books(favorites)

        print("\n--- Рекомендации на основе прочитанного и избранного ---")
        liked_genres = [b['genre'] for b in self.books if b['is_read'] or b['is_favorite']]
        if not liked_genres:
            print("Недостаточно данных для рекомендаций.")
            return

        most_common_genre = Counter(liked_genres).most_common(1)[0][0]
        recommendations = [b for b in self.books if b['genre'] == most_common_genre and not b['is_read']]
        
        if recommendations:
            print(f"Вам нравится жанр '{most_common_genre}'. Возможно, вам будет интересно:")
            self.display_books(recommendations)
        else:
            print(f"В жанре '{most_common_genre}' пока нет непрочитанных книг.")

    def run(self):
        while True:
            print("\n" + "="*20)
            print("Т-Библиотека")
            print("="*20)
            print("1. Добавить книгу")
            print("2. Просмотр и фильтрация книг")
            print("3. Управление книгой (статус, избранное, удаление)")
            print("4. Поиск книг")
            print("5. Избранное и рекомендации")
            print("0. Выход")
            
            choice = input("\nВыберите пункт меню: ").strip()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.view_and_filter_books()
            elif choice == '3':
                self.manage_book()
            elif choice == '4':
                self.search_books()
            elif choice == '5':
                self.show_favorites_and_recommendations()
            elif choice == '0':
                print("Выход из программы...")
                break
            else:
                print("Неизвестная команда.")

if __name__ == "__main__":
    app = TLibrary()
    app.run()
