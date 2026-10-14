"""
Console User Interface - Simplified
"""

import os
import sys
from services.library_service import LibraryService


class ConsoleUI:
    """Console-based user interface"""
    
    def __init__(self):
        self.library = LibraryService()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self, title: str):
        self.clear_screen()
        print("=" * 60)
        print(f"  📚 {title}")
        print("=" * 60)
        print()
        
    def display_menu(self):
        self.display_header("LIBRARY MANAGEMENT SYSTEM")
        print("1.  Add New Book")
        print("2.  View All Books")
        print("3.  Search Books")
        print("4.  Borrow Book")
        print("5.  Return Book")
        print("6.  View Current Borrowings")
        print("7.  View All Users")
        print("8.  Library Statistics")
        print("9.  Exit")
        print()
        print("-" * 60)
        
    def get_input(self, prompt: str, required: bool = True) -> str:
        while True:
            value = input(prompt).strip()
            if required and not value:
                print("This field is required. Please try again.")
                continue
            return value
            
    def get_int_input(self, prompt: str, min_val: int = 1) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number")
                
    def display_table(self, headers, rows):
        if not rows:
            print("No data to display")
            return
            
        # Simple table display
        for header in headers:
            print(f"{header:<20}", end="")
        print()
        print("-" * (20 * len(headers)))
        
        for row in rows[:20]:
            for cell in row:
                print(f"{str(cell)[:18]:<20}", end="")
            print()
            
    # ============ MENU HANDLERS ============
    
    def handle_add_book(self):
        self.display_header("ADD NEW BOOK")
        title = self.get_input("Title: ")
        author = self.get_input("Author: ")
        isbn = self.get_input("ISBN: ")
        category = self.get_input("Category: ")
        copies = self.get_int_input("Number of copies: ")
        
        book_id = self.library.add_book(title, author, isbn, category, copies)
        if book_id:
            print(f"\n✅ Book added successfully! ID: {book_id}")
        else:
            print("\n❌ Failed to add book")
        input("\nPress Enter to continue...")
        
    def handle_view_books(self):
        self.display_header("ALL BOOKS")
        books = self.library.get_all_books()
        
        if books:
            headers = ['ID', 'Title', 'Author', 'Available']
            rows = []
            for book in books:
                rows.append([
                    book['book_id'][:6],
                    book['title'][:25],
                    book['author'][:20],
                    f"{book['available_copies']}/{book['total_copies']}"
                ])
            self.display_table(headers, rows)
        else:
            print("No books in the library")
        input("\nPress Enter to continue...")
        
    def handle_search_books(self):
        self.display_header("SEARCH BOOKS")
        keyword = self.get_input("Enter search keyword: ", required=False)
        
        if not keyword:
            books = self.library.get_all_books()
        else:
            books = self.library.search_books(keyword)
            
        if books:
            print(f"\nFound {len(books)} book(s)")
            for book in books:
                print(f"  {book['title']} by {book['author']} - {book['available_copies']} available")
        else:
            print("No books found")
        input("\nPress Enter to continue...")
        
    def handle_borrow_book(self):
        self.display_header("BORROW BOOK")
        user_id = self.get_input("User ID: ")
        book_id = self.get_input("Book ID: ")
        
        if self.library.borrow_book(user_id, book_id):
            print("\n✅ Book borrowed successfully!")
        else:
            print("\n❌ Failed to borrow book")
        input("\nPress Enter to continue...")
        
    def handle_return_book(self):
        self.display_header("RETURN BOOK")
        user_id = self.get_input("User ID: ")
        book_id = self.get_input("Book ID: ")
        
        if self.library.return_book(user_id, book_id):
            print("\n✅ Book returned successfully!")
        else:
            print("\n❌ Failed to return book")
        input("\nPress Enter to continue...")
        
    def handle_view_borrowings(self):
        self.display_header("CURRENT BORROWINGS")
        borrowings = self.library.get_current_borrowings()
        
        if borrowings:
            for b in borrowings:
                status = "OVERDUE" if b.get('days_overdue', 0) > 0 else "Active"
                print(f"  {b['title']} - {b['user_name']} - {status}")
        else:
            print("No active borrowings")
        input("\nPress Enter to continue...")
        
    def handle_view_users(self):
        self.display_header("ALL USERS")
        users = self.library.get_all_users()
        
        if users:
            for user in users:
                print(f"  {user['name']} - {user['email']}")
        else:
            print("No users registered")
        input("\nPress Enter to continue...")
        
    def handle_statistics(self):
        self.display_header("LIBRARY STATISTICS")
        stats = self.library.get_statistics()
        
        print(f"  Total Books:         {stats.get('total_books', 0)}")
        print(f"  Active Users:        {stats.get('active_users', 0)}")
        print(f"  Active Borrowings:   {stats.get('active_borrowings', 0)}")
        print(f"  Overdue Books:       {stats.get('overdue_books', 0)}")
        print(f"  Total Transactions:  {stats.get('total_transactions', 0)}")
        
        print("\n  Books by Category:")
        for cat in stats.get('books_by_category', []):
            print(f"    {cat['category']}: {cat['count']}")
            
        print("\n  Most Borrowed Books:")
        for book in stats.get('most_borrowed', [])[:5]:
            print(f"    {book['title']} - {book['borrow_count']} times")
            
        input("\nPress Enter to continue...")
        
    def exit_app(self):
        self.display_header("GOODBYE!")
        print("Thank you for using the Library Management System!")
        sys.exit(0)
        
    # ============ MAIN LOOP ============
    
    def run(self):
        while True:
            self.display_menu()
            choice = self.get_input("Enter your choice (1-9): ", required=False)
            
            handlers = {
                '1': self.handle_add_book,
                '2': self.handle_view_books,
                '3': self.handle_search_books,
                '4': self.handle_borrow_book,
                '5': self.handle_return_book,
                '6': self.handle_view_borrowings,
                '7': self.handle_view_users,
                '8': self.handle_statistics,
                '9': self.exit_app
            }
            
            handler = handlers.get(choice)
            if handler:
                handler()
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("\nPress Enter to continue...")