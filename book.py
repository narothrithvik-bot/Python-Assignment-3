import json
import logging
from pathlib import Path

# -----------------------------------------------------------
# Setup Logging
# -----------------------------------------------------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------------
# Book Class
# -----------------------------------------------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status  # available / issued

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def issue(self):
        """Issue the book if available."""
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        """Return the book if it was issued."""
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"

    def to_dict(self):
        """Convert Book object to dictionary (JSON serializable)."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Create a Book object from a dictionary."""
        return Book(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            status=data["status"]
        )

# -----------------------------------------------------------
# Library Inventory Class
# -----------------------------------------------------------
class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()

    def load_books(self):
        """Load books from JSON file."""
        try:
            if self.file_path.exists():
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                logging.info("Catalog loaded successfully.")
            else:
                self.books = []
                self.save_books()
        except Exception as e:
            logging.error(f"Error loading catalog: {e}")
            self.books = []

    def save_books(self):
        """Save all books to JSON."""
        try:
            with open(self.file_path, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
            logging.info("Catalog saved.")
        except Exception as e:
            logging.error(f"Could not save catalog: {e}")

    # ---------------- Inventory operations ----------------

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books

# -----------------------------------------------------------
# CLI Menu
# -----------------------------------------------------------
def menu():
    print("\n===== Library Inventory Manager =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Enter your choice: ")

# -----------------------------------------------------------
# Main Application
# -----------------------------------------------------------
def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        try:
            # Add Book
            if choice == "1":
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                isbn = input("Enter ISBN: ")
                book = Book(title, author, isbn)
                inventory.add_book(book)
                print("Book added successfully!")

            # Issue Book
            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_books()
                    print("Book issued successfully!")
                else:
                    print("Book not available or not found.")

            # Return Book
            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_books()
                    print("Book returned successfully!")
                else:
                    print("Cannot return book or book not found.")

            # View All
            elif choice == "4":
                books = inventory.display_all()
                if not books:
                    print("No books in catalog.")
                else:
                    for b in books:
                        print(b)

            # Search
            elif choice == "5":
                title = input("Enter title to search: ")
                results = inventory.search_by_title(title)
                if results:
                    for b in results:
                        print(b)
                else:
                    print("No books found.")

            # Exit
            elif choice == "6":
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1–6.")

        except Exception as e:
            print("Error occurred:", e)
            logging.error(f"Runtime error: {e}")

# -----------------------------------------------------------
# Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    main()