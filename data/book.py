import json

# Load book data from JSON file
def load_books():
    with open('data/book_data.json', 'r') as file:  # Thay đổi đường dẫn nếu cần
        return json.load(file)['books']

# Save book data to JSON file
def save_books(books):
    with open('data/book_data.json', 'w') as file:
        json.dump({"books": books}, file, indent=4)

# Search for books by title
def search_books_by_title(title):
    books = load_books()
    return [book for book in books if title.lower() in book['title'].lower()]

# Search for books by author
def search_books_by_author(author):
    books = load_books()
    return [book for book in books if author.lower() in book['author'].lower()]

# Sort books by title
def sort_books_by_title():
    books = load_books()
    return sorted(books, key=lambda x: x['title'])

# Sort books by author
def sort_books_by_author():
    books = load_books()
    return sorted(books, key=lambda x: x['author'])

# Add a new book
def add_book(new_book):
    books = load_books()
    books.append(new_book)
    save_books(books)

# Delete a book by ID
def delete_book(book_id):
    books = load_books()
    books = [book for book in books if book['id'] != book_id]
    save_books(books)

# Search for books by genre
def search_books_by_genre(genre):
    books = load_books()
    return [book for book in books if genre.lower() in (g.lower() for g in book['genre'])]

# Match books by multiple genres
def match_books_by_genres(genres):
    books = load_books()
    return [book for book in books if any(genre.lower() in (g.lower() for g in book['genre']) for genre in genres)]