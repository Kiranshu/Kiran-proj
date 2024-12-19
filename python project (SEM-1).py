import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class LibraryManagementSystem:
    def __init__(self):
        # Initialize data for books and users
        self.books = pd.DataFrame(columns=["BookID", "Title", "Author", "Genre", "Available"])
        self.users = pd.DataFrame(columns=["UserID", "Name", "BorrowedBooks"])
        self.transactions = pd.DataFrame(columns=["TransactionID", "UserID", "BookID", "Action", "Date"])
        self.transaction_id = 1

    # ----------------------------- Book Management ----------------------------- #
    def add_book(self, title, author, genre):
        """Add a new book to the library."""
        book_id = len(self.books) + 1
        new_book = pd.DataFrame({
            "BookID": [book_id],
            "Title": [title],
            "Author": [author],
            "Genre": [genre],
            "Available": [True]
        })
        self.books = pd.concat([self.books, new_book], ignore_index=True)
        print(f"Book '{title}' added successfully!")

    def remove_book(self, book_id):
        """Remove a book from the library."""
        if book_id in self.books["BookID"].values:
            self.books = self.books[self.books["BookID"] != book_id]
            print(f"Book with ID {book_id} removed successfully!")
        else:
            print(f"Book with ID {book_id} not found!")

    def lend_book(self, user_id, book_id):
        """Lend a book to a user."""
        if user_id not in self.users["UserID"].values:
            print(f"User with ID {user_id} does not exist.")
            return

        if book_id in self.books["BookID"].values:
            book_idx = self.books[self.books["BookID"] == book_id].index[0]
            if self.books.at[book_idx, "Available"]:
                # Update book availability
                self.books.at[book_idx, "Available"] = False
                # Update user record
                user_idx = self.users[self.users["UserID"] == user_id].index[0]
                self.users.at[user_idx, "BorrowedBooks"].append(book_id)
                # Record transaction
                self._record_transaction(user_id, book_id, "Lend")
                print(f"Book ID {book_id} has been lent to User ID {user_id}.")
            else:
                print(f"Book ID {book_id} is currently not available.")
        else:
            print(f"Book ID {book_id} does not exist.")

    def return_book(self, user_id, book_id):
        """Return a book to the library."""
        if user_id in self.users["UserID"].values:
            user_idx = self.users[self.users["UserID"] == user_id].index[0]
            if book_id in self.users.at[user_idx, "BorrowedBooks"]:
                # Update book availability
                book_idx = self.books[self.books["BookID"] == book_id].index[0]
                self.books.at[book_idx, "Available"] = True
                # Update user record
                self.users.at[user_idx, "BorrowedBooks"].remove(book_id)
                # Record transaction
                self._record_transaction(user_id, book_id, "Return")
                print(f"Book ID {book_id} returned by User ID {user_id}.")
            else:
                print(f"User ID {user_id} has not borrowed Book ID {book_id}.")
        else:
            print(f"User ID {user_id} does not exist.")

    # ----------------------------- User Management ----------------------------- #
    def add_user(self, name):
        """Add a new user to the library system."""
        user_id = len(self.users) + 1
        new_user = pd.DataFrame({
            "UserID": [user_id],
            "Name": [name],
            "BorrowedBooks": [[]]
        })
        self.users = pd.concat([self.users, new_user], ignore_index=True)
        print(f"User '{name}' added successfully!")

    def remove_user(self, user_id):
        """Remove a user from the library system."""
        if user_id in self.users["UserID"].values:
            self.users = self.users[self.users["UserID"] != user_id]
            print(f"User with ID {user_id} removed successfully!")
        else:
            print(f"User with ID {user_id} not found!")

    # ----------------------------- Data Visualization ----------------------------- #
    def visualize_books_by_genre(self):
        """Visualize the number of books by genre."""
        genre_counts = self.books["Genre"].value_counts()
        genre_counts.plot(kind="bar", color="skyblue")
        plt.title("Books by Genre")
        plt.xlabel("Genre")
        plt.ylabel("Number of Books")
        plt.show()

    def visualize_user_borrowing(self):
        """Visualize user borrowing activity."""
        user_borrow_counts = self.users["BorrowedBooks"].apply(len)
        user_borrow_counts.plot(kind="bar", color="orange")
        plt.title("Books Borrowed by Users")
        plt.xlabel("User ID")
        plt.ylabel("Number of Books Borrowed")
        plt.show()

    def visualize_book_availability(self):
        """Visualize book availability."""
        availability_counts = self.books["Available"].value_counts()
        availability_counts.index = ["Available", "Not Available"]
        availability_counts.plot(kind="pie", autopct="%1.1f%%", colors=["green", "red"])
        plt.title("Book Availability")
        plt.show()

    # ----------------------------- Private Methods ----------------------------- #
    def _record_transaction(self, user_id, book_id, action):
        """Record a lending or returning transaction."""
        new_transaction = pd.DataFrame({
            "TransactionID": [self.transaction_id],
            "UserID": [user_id],
            "BookID": [book_id],
            "Action": [action],
            "Date": [pd.Timestamp.now()]
        })
        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        self.transaction_id += 1


# ----------------------------- Example Usage ----------------------------- #
if __name__ == "__main__":
    library = LibraryManagementSystem()

    # Add users
    library.add_user("Alice")
    library.add_user("Bob")

    # Add books
    library.add_book("1984", "George Orwell", "Fiction")
    library.add_book("A Brief History of Time", "Stephen Hawking", "Science")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction")

    # Lend books
    library.lend_book(1, 1)  # Alice borrows "1984"
    library.lend_book(2, 2)  # Bob borrows "A Brief History of Time"

    # Return books
    library.return_book(1, 1)  # Alice returns "1984"

    # Visualizations
    library.visualize_books_by_genre()
    library.visualize_user_borrowing()
    library.visualize_book_availability()
