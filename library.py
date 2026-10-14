"""
LIBRARY MANAGEMENT SYSTEM - COMPLETE WORKING VERSION
"""

import sqlite3
import os
import uuid
from datetime import datetime, timedelta
import sys

# ============================================
# SETUP DATABASE
# ============================================

def setup_database():
    """Create database and sample data"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            member_since DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            due_date DATETIME,
            returned_at DATETIME,
            status TEXT DEFAULT 'BORROWED'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            book_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data
    books = [
        ('BK001', 'The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 3, 3),
        ('BK002', 'To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 2, 2),
        ('BK003', '1984', 'George Orwell', '978-0-452-28423-4', 'Science Fiction', 4, 4),
        ('BK004', 'Python Programming', 'John Smith', '978-1-234-56789-0', 'Technology', 5, 5),
        ('BK005', 'The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 3, 3),
    ]
    
    for book in books:
        cursor.execute('INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', book)
    
    users = [
        ('US001', 'Alice Johnson', 'alice@email.com', '555-0101'),
        ('US002', 'Bob Smith', 'bob@email.com', '555-0102'),
        ('US003', 'Carol White', 'carol@email.com', '555-0103'),
    ]
    
    for user in users:
        cursor.execute('INSERT OR IGNORE INTO users (user_id, name, email, phone) VALUES (?, ?, ?, ?)', user)
    
    conn.commit()
    conn.close()
    print("✅ Database setup complete!")

# ============================================
# MAIN SYSTEM
# ============================================

class LibrarySystem:
    def __init__(self):
        setup_database()
        self.conn = sqlite3.connect('library.db')
        self.conn.row_factory = sqlite3.Row
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_menu(self):
        self.clear_screen()
        print("=" * 60)
        print("  📚 LIBRARY MANAGEMENT SYSTEM")
        print("=" * 60)
        print("\n1. View All Books")
        print("2. Add New Book")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Borrowings")
        print("7. View Users")
        print("8. Add User")
        print("9. Statistics")
        print("10. Exit")
        print("\n" + "-" * 60)
        
    def get_number_input(self, prompt, min_val=1):
        """Get number input with validation"""
        while True:
            value = input(prompt).strip()
            if value == "":
                print("❌ Please enter a number. Try again.")
                continue
            try:
                num = int(value)
                if num < min_val:
                    print(f"❌ Value must be at least {min_val}. Try again.")
                    continue
                return num
            except ValueError:
                print("❌ Please enter a valid number. Try again.")
        
    def view_books(self):
        self.clear_screen()
        print("ALL BOOKS\n" + "=" * 40)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY title')
        books = cursor.fetchall()
        
        if books:
            for book in books:
                status = "✅ Available" if book['available_copies'] > 0 else "❌ Unavailable"
                print(f"\nID: {book['book_id']}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print(f"Category: {book['category']}")
                print(f"Copies: {book['available_copies']}/{book['total_copies']}")
                print(f"Status: {status}")
                print("-" * 30)
        else:
            print("No books found")
            
        input("\nPress Enter to continue...")
        
    def add_book(self):
        self.clear_screen()
        print("ADD NEW BOOK\n" + "=" * 40)
        
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        category = input("Category: ")
        copies = self.get_number_input("Number of copies: ")
        
        book_id = str(uuid.uuid4())[:8]
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (book_id, title, author, isbn, category, copies, copies))
            self.conn.commit()
            print(f"\n✅ Book added! ID: {book_id}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            
        input("\nPress Enter to continue...")
        
    def search_books(self):
        self.clear_screen()
        print("SEARCH BOOKS\n" + "=" * 40)
        
        keyword = input("Enter search keyword: ").lower()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM books 
            WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(category) LIKE ?
            ORDER BY title
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        books = cursor.fetchall()
        
        if books:
            print(f"\nFound {len(books)} book(s):")
            for book in books:
                print(f"\n  {book['title']} by {book['author']}")
                print(f"  {book['available_copies']} copies available")
                print(f"  ID: {book['book_id']}")
        else:
            print("\nNo books found")
            
        input("\nPress Enter to continue...")
        
    def borrow_book(self):
        self.clear_screen()
        print("BORROW BOOK\n" + "=" * 40)
        
        # Show available books
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books WHERE available_copies > 0')
        available = cursor.fetchall()
        
        if not available:
            print("No books available!")
            input("\nPress Enter to continue...")
            return
            
        print("Available Books:")
        for book in available:
            print(f"  {book['book_id']} - {book['title']} ({book['available_copies']} copies)")
            
        user_id = input("\nEnter User ID: ")
        book_id = input("Enter Book ID: ")
        
        cursor = self.conn.cursor()
        cursor.execute('BEGIN')
        
        try:
            # Check if book available
            cursor.execute('SELECT available_copies FROM books WHERE book_id = ?', (book_id,))
            if not cursor.fetchone():
                print("❌ Book not found")
                self.conn.rollback()
                input("\nPress Enter to continue...")
                return
                
            # Check if user exists
            cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
            if not cursor.fetchone():
                print("❌ User not found")
                self.conn.rollback()
                input("\nPress Enter to continue...")
                return
                
            # Check if already borrowed
            cursor.execute('''
                SELECT COUNT(*) as count FROM borrowings 
                WHERE user_id = ? AND book_id = ? AND status = 'BORROWED'
            ''', (user_id, book_id))
            if cursor.fetchone()['count'] > 0:
                print("❌ User already has this book")
                self.conn.rollback()
                input("\nPress Enter to continue...")
                return
                
            # Borrow the book
            cursor.execute('UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?', (book_id,))
            
            due_date = datetime.now() + timedelta(days=14)
            cursor.execute('''
                INSERT INTO borrowings (book_id, user_id, due_date)
                VALUES (?, ?, ?)
            ''', (book_id, user_id, due_date.isoformat()))
            
            trans_id = str(uuid.uuid4())[:8]
            cursor.execute('''
                INSERT INTO transactions (transaction_id, book_id, user_id, transaction_type)
                VALUES (?, ?, ?, 'BORROW')
            ''', (trans_id, book_id, user_id))
            
            self.conn.commit()
            print("\n✅ Book borrowed successfully!")
            
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: {e}")
            
        input("\nPress Enter to continue...")
        
    def return_book(self):
        self.clear_screen()
        print("RETURN BOOK\n" + "=" * 40)
        
        user_id = input("Enter User ID: ")
        book_id = input("Enter Book ID: ")
        
        cursor = self.conn.cursor()
        cursor.execute('BEGIN')
        
        try:
            # Check if borrowed
            cursor.execute('''
                SELECT borrowing_id FROM borrowings 
                WHERE user_id = ? AND book_id = ? AND status = 'BORROWED'
            ''', (user_id, book_id))
            
            if not cursor.fetchone():
                print("❌ This user hasn't borrowed this book")
                self.conn.rollback()
                input("\nPress Enter to continue...")
                return
                
            # Return the book
            cursor.execute('''
                UPDATE borrowings SET returned_at = CURRENT_TIMESTAMP, status = 'RETURNED'
                WHERE user_id = ? AND book_id = ? AND status = 'BORROWED'
            ''', (user_id, book_id))
            
            cursor.execute('UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?', (book_id,))
            
            trans_id = str(uuid.uuid4())[:8]
            cursor.execute('''
                INSERT INTO transactions (transaction_id, book_id, user_id, transaction_type)
                VALUES (?, ?, ?, 'RETURN')
            ''', (trans_id, book_id, user_id))
            
            self.conn.commit()
            print("\n✅ Book returned successfully!")
            
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: {e}")
            
        input("\nPress Enter to continue...")
        
    def view_borrowings(self):
        self.clear_screen()
        print("CURRENT BORROWINGS\n" + "=" * 40)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT b.title, b.author, u.name as user_name, br.borrowed_at, br.due_date
            FROM borrowings br
            JOIN books b ON br.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE br.status = 'BORROWED'
            ORDER BY br.borrowed_at
        ''')
        
        borrowings = cursor.fetchall()
        
        if borrowings:
            for b in borrowings:
                print(f"\n  {b['title']} by {b['author']}")
                print(f"  Borrowed by: {b['user_name']}")
                print(f"  Due: {b['due_date'][:10]}")
                print("-" * 30)
        else:
            print("No active borrowings")
            
        input("\nPress Enter to continue...")
        
    def view_users(self):
        self.clear_screen()
        print("ALL USERS\n" + "=" * 40)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY name')
        users = cursor.fetchall()
        
        if users:
            for user in users:
                print(f"\n  ID: {user['user_id']}")
                print(f"  Name: {user['name']}")
                print(f"  Email: {user['email']}")
                print(f"  Phone: {user['phone']}")
                print("-" * 30)
        else:
            print("No users found")
            
        input("\nPress Enter to continue...")
        
    def add_user(self):
        self.clear_screen()
        print("ADD NEW USER\n" + "=" * 40)
        
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        
        user_id = str(uuid.uuid4())[:8]
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (user_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            ''', (user_id, name, email, phone))
            self.conn.commit()
            print(f"\n✅ User added! ID: {user_id}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            
        input("\nPress Enter to continue...")
        
    def show_statistics(self):
        self.clear_screen()
        print("LIBRARY STATISTICS\n" + "=" * 40)
        
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM books')
        total_books = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1')
        total_users = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM borrowings WHERE status = "BORROWED"')
        active_borrowings = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM borrowings 
            WHERE status = "BORROWED" AND due_date < CURRENT_TIMESTAMP
        ''')
        overdue = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT category, COUNT(*) as count FROM books GROUP BY category
        ''')
        categories = cursor.fetchall()
        
        print(f"\n  📊 Summary")
        print(f"  {'-' * 30}")
        print(f"  Total Books:        {total_books}")
        print(f"  Total Users:        {total_users}")
        print(f"  Active Borrowings:  {active_borrowings}")
        print(f"  Overdue Books:      {overdue}")
        
        print(f"\n  📚 Books by Category")
        print(f"  {'-' * 30}")
        for cat in categories:
            print(f"  {cat['category']}: {cat['count']}")
            
        input("\nPress Enter to continue...")
        
    def run(self):
        while True:
            self.show_menu()
            choice = input("\nEnter choice (1-10): ")
            
            if choice == '1':
                self.view_books()
            elif choice == '2':
                self.add_book()
            elif choice == '3':
                self.search_books()
            elif choice == '4':
                self.borrow_book()
            elif choice == '5':
                self.return_book()
            elif choice == '6':
                self.view_borrowings()
            elif choice == '7':
                self.view_users()
            elif choice == '8':
                self.add_user()
            elif choice == '9':
                self.show_statistics()
            elif choice == '10':
                self.clear_screen()
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
                
        self.conn.close()

# ============================================
# RUN THE SYSTEM
# ============================================

if __name__ == "__main__":
    try:
        system = LibrarySystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()