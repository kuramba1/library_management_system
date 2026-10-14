"""
Database Manager - Handles all database operations for SQLite
"""

import sqlite3
import os
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import uuid


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str = 'data/library.db'):
        self.db_path = db_path
        self.ensure_database()
        
    def ensure_database(self):
        """Ensure database directory exists and initialize schema"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Check if database exists
        if not os.path.exists(self.db_path):
            self.create_tables()
            self.insert_sample_data()
            
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def create_tables(self):
        """Create all tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Books table - Using your schema but with DATETIME instead of TIMESTAMP
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id VARCHAR(8) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                isbn VARCHAR(20) UNIQUE NOT NULL,
                category VARCHAR(100) NOT NULL,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(8) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                member_since DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Borrowings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowings (
                borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id VARCHAR(8) NOT NULL,
                user_id VARCHAR(8) NOT NULL,
                borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                due_date DATETIME,
                returned_at DATETIME,
                status VARCHAR(20) DEFAULT 'BORROWED',
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id VARCHAR(8) PRIMARY KEY,
                book_id VARCHAR(8) NOT NULL,
                user_id VARCHAR(8) NOT NULL,
                transaction_type VARCHAR(10) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'COMPLETED',
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_category ON books(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_book_id ON transactions(book_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_borrowings_user_id ON borrowings(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_borrowings_book_id ON borrowings(book_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_borrowings_status ON borrowings(status)')
        
        conn.commit()
        conn.close()
        
    def insert_sample_data(self):
        """Insert sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sample books
        books = [
            ('BK001', 'The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 3, 3),
            ('BK002', 'To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 2, 2),
            ('BK003', '1984', 'George Orwell', '978-0-452-28423-4', 'Science Fiction', 4, 4),
            ('BK004', 'Python Programming', 'John Smith', '978-1-234-56789-0', 'Technology', 5, 5),
            ('BK005', 'The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 3, 3),
            ('BK006', 'Data Science 101', 'Jane Smith', '978-1-234-56789-1', 'Technology', 2, 2),
        ]
        
        for book in books:
            cursor.execute('''
                INSERT OR IGNORE INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', book)
            
        # Sample users
        users = [
            ('US001', 'Alice Johnson', 'alice@email.com', '555-0101'),
            ('US002', 'Bob Smith', 'bob@email.com', '555-0102'),
            ('US003', 'Carol White', 'carol@email.com', '555-0103'),
            ('US004', 'David Brown', 'david@email.com', '555-0104'),
        ]
        
        for user in users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            ''', user)
            
        conn.commit()
        conn.close()
        
    # ============ BOOK OPERATIONS ============
    
    def add_book(self, title: str, author: str, isbn: str, 
                 category: str, total_copies: int = 1) -> Optional[str]:
        """Add a new book to the library"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            book_id = str(uuid.uuid4())[:8]
            
            cursor.execute('''
                INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (book_id, title, author, isbn, category, total_copies, total_copies))
            
            conn.commit()
            conn.close()
            return book_id
            
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e):
                print(f"Error: ISBN '{isbn}' already exists in the system")
            else:
                print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Error adding book: {e}")
            return None
            
    def get_all_books(self) -> List[Dict]:
        """Get all books"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books ORDER BY title')
        books = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return books
        
    def search_books(self, keyword: str) -> List[Dict]:
        """Search books by title, author, ISBN, or category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_term = f'%{keyword.lower()}%'
        cursor.execute('''
            SELECT * FROM books 
            WHERE LOWER(title) LIKE ? 
               OR LOWER(author) LIKE ? 
               OR LOWER(isbn) LIKE ?
               OR LOWER(category) LIKE ?
            ORDER BY title
        ''', (search_term, search_term, search_term, search_term))
        
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books
        
    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        """Get a specific book by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book = cursor.fetchone()
        
        conn.close()
        return dict(book) if book else None
        
    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        """Get a book by ISBN"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
        book = cursor.fetchone()
        
        conn.close()
        return dict(book) if book else None
        
    def update_book(self, book_id: str, **kwargs) -> bool:
        """Update book information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            allowed_fields = ['title', 'author', 'isbn', 'category', 'total_copies']
            for key, value in kwargs.items():
                if key in allowed_fields and value is not None:
                    updates.append(f"{key} = ?")
                    values.append(value)
                    
            if not updates:
                return False
                
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(book_id)
            
            query = f"UPDATE books SET {', '.join(updates)} WHERE book_id = ?"
            cursor.execute(query, values)
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
            
    def update_availability(self, book_id: str, change: int) -> bool:
        """Update available copies (increment or decrement)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE books 
                SET available_copies = available_copies + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE book_id = ? 
                AND available_copies + ? >= 0
            ''', (change, book_id, change))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            print(f"Error updating availability: {e}")
            return False
            
    def delete_book(self, book_id: str) -> bool:
        """Delete a book if not borrowed"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if book is currently borrowed
            cursor.execute('''
                SELECT COUNT(*) as count FROM borrowings 
                WHERE book_id = ? AND status = 'BORROWED'
            ''', (book_id,))
            
            if cursor.fetchone()['count'] > 0:
                print("Cannot delete: Book is currently borrowed")
                conn.close()
                return False
                
            cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
            
    def get_books_by_category(self, category: str) -> List[Dict]:
        """Get books by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM books 
            WHERE LOWER(category) = LOWER(?)
            ORDER BY title
        ''', (category,))
        
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books
        
    def is_book_available(self, book_id: str) -> bool:
        """Check if book is available"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT available_copies > 0 as available 
            FROM books WHERE book_id = ?
        ''', (book_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result['available'] if result else False
        
    # ============ USER OPERATIONS ============
    
    def add_user(self, name: str, email: str, phone: str) -> Optional[str]:
        """Add a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            user_id = str(uuid.uuid4())[:8]
            
            cursor.execute('''
                INSERT INTO users (user_id, name, email, phone)
                VALUES (?, ?, ?, ?)
            ''', (user_id, name, email, phone))
            
            conn.commit()
            conn.close()
            return user_id
            
        except sqlite3.IntegrityError:
            print(f"Error: Email '{email}' is already registered")
            return None
        except Exception as e:
            print(f"Error adding user: {e}")
            return None
            
    def get_all_users(self) -> List[Dict]:
        """Get all active users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY name')
        users = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return users
        
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
        
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
        
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            updates = []
            values = []
            
            allowed_fields = ['name', 'email', 'phone']
            for key, value in kwargs.items():
                if key in allowed_fields and value is not None:
                    updates.append(f"{key} = ?")
                    values.append(value)
                    
            if not updates:
                return False
                
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, values)
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
            
    def delete_user(self, user_id: str) -> bool:
        """Soft delete a user (deactivate)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user has active borrowings
            cursor.execute('''
                SELECT COUNT(*) as count FROM borrowings 
                WHERE user_id = ? AND status = 'BORROWED'
            ''', (user_id,))
            
            if cursor.fetchone()['count'] > 0:
                print("Cannot delete: User has borrowed books")
                conn.close()
                return False
                
            cursor.execute('UPDATE users SET is_active = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
            
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
            
    # ============ BORROWING OPERATIONS ============
    
    def borrow_book(self, user_id: str, book_id: str) -> bool:
        """Process book borrowing"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Start transaction
            cursor.execute('BEGIN')
            
            # 1. Check if book is available
            cursor.execute('''
                SELECT available_copies FROM books 
                WHERE book_id = ? AND available_copies > 0
            ''', (book_id,))
            
            if not cursor.fetchone():
                conn.rollback()
                conn.close()
                print("No copies available")
                return False
                
            # 2. Check if user exists and is active
            cursor.execute('''
                SELECT user_id FROM users 
                WHERE user_id = ? AND is_active = 1
            ''', (user_id,))
            
            if not cursor.fetchone():
                conn.rollback()
                conn.close()
                print("User not found or inactive")
                return False
                
            # 3. Check if user already has this book
            cursor.execute('''
                SELECT COUNT(*) as count FROM borrowings 
                WHERE user_id = ? AND book_id = ? AND status = 'BORROWED'
            ''', (user_id, book_id))
            
            if cursor.fetchone()['count'] > 0:
                conn.rollback()
                conn.close()
                print("User already has this book")
                return False
                
            # 4. Update book availability
            cursor.execute('''
                UPDATE books 
                SET available_copies = available_copies - 1
                WHERE book_id = ?
            ''', (book_id,))
            
            # 5. Create borrowing record
            due_date = datetime.now() + timedelta(days=14)  # 2 weeks
            
            cursor.execute('''
                INSERT INTO borrowings (book_id, user_id, due_date)
                VALUES (?, ?, ?)
            ''', (book_id, user_id, due_date.isoformat()))
            
            # 6. Create transaction record
            transaction_id = str(uuid.uuid4())[:8]
            cursor.execute('''
                INSERT INTO transactions (transaction_id, book_id, user_id, transaction_type)
                VALUES (?, ?, ?, 'BORROW')
            ''', (transaction_id, book_id, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error borrowing book: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
            
    def return_book(self, user_id: str, book_id: str) -> bool:
        """Process book return"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('BEGIN')
            
            # 1. Check if user has this book borrowed
            cursor.execute('''
                SELECT borrowing_id FROM borrowings 
                WHERE user_id = ? AND book_id = ? AND status = 'BORROWED'
            ''', (user_id, book_id))
            
            borrowing = cursor.fetchone()
            if not borrowing:
                conn.rollback()
                conn.close()
                print("User hasn't borrowed this book")
                return False
                
            # 2. Update borrowing record
            cursor.execute('''
                UPDATE borrowings 
                SET returned_at = CURRENT_TIMESTAMP,
                    status = 'RETURNED'
                WHERE borrowing_id = ?
            ''', (borrowing['borrowing_id'],))
            
            # 3. Update book availability
            cursor.execute('''
                UPDATE books 
                SET available_copies = available_copies + 1
                WHERE book_id = ?
            ''', (book_id,))
            
            # 4. Create transaction record
            transaction_id = str(uuid.uuid4())[:8]
            cursor.execute('''
                INSERT INTO transactions (transaction_id, book_id, user_id, transaction_type)
                VALUES (?, ?, ?, 'RETURN')
            ''', (transaction_id, book_id, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error returning book: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
            
    # ============ TRANSACTION HISTORY ============
    
    def get_transaction_history(self, user_id: Optional[str] = None, 
                                limit: int = 50) -> List[Dict]:
        """Get transaction history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT t.*, b.title as book_title, u.name as user_name
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                JOIN users u ON t.user_id = u.user_id
                WHERE t.user_id = ?
                ORDER BY t.timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT t.*, b.title as book_title, u.name as user_name
                FROM transactions t
                JOIN books b ON t.book_id = b.book_id
                JOIN users u ON t.user_id = u.user_id
                ORDER BY t.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions
        
    def get_user_borrowing_history(self, user_id: str) -> List[Dict]:
        """Get complete borrowing history for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.*, br.borrowed_at, br.due_date, br.returned_at, br.status
            FROM borrowings br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.user_id = ?
            ORDER BY br.borrowed_at DESC
        ''', (user_id,))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return history
        
    def get_current_borrowings(self) -> List[Dict]:
        """Get all currently borrowed books"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                b.book_id, b.title, b.author, b.isbn,
                u.user_id, u.name as user_name, u.email,
                br.borrowed_at, br.due_date,
                julianday('now') - julianday(br.due_date) as days_overdue
            FROM borrowings br
            JOIN books b ON br.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE br.status = 'BORROWED'
            ORDER BY br.borrowed_at DESC
        ''')
        
        borrowings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return borrowings
        
    def get_overdue_books(self) -> List[Dict]:
        """Get all overdue books"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                b.*, u.name as user_name, u.email, u.phone,
                br.borrowed_at, br.due_date,
                julianday('now') - julianday(br.due_date) as days_overdue
            FROM borrowings br
            JOIN books b ON br.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE br.status = 'BORROWED' 
            AND br.due_date < CURRENT_TIMESTAMP
            ORDER BY br.due_date
        ''')
        
        overdue = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return overdue
        
    # ============ STATISTICS & REPORTS ============
    
    def get_statistics(self) -> Dict:
        """Get library statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total books
        cursor.execute('SELECT COUNT(*) as count FROM books')
        stats['total_books'] = cursor.fetchone()['count']
        
        # Total unique titles
        cursor.execute('SELECT COUNT(DISTINCT title) as count FROM books')
        stats['unique_titles'] = cursor.fetchone()['count']
        
        # Total users
        cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1')
        stats['active_users'] = cursor.fetchone()['count']
        
        # Current borrowings
        cursor.execute('SELECT COUNT(*) as count FROM borrowings WHERE status = "BORROWED"')
        stats['active_borrowings'] = cursor.fetchone()['count']
        
        # Overdue books
        cursor.execute('''
            SELECT COUNT(*) as count FROM borrowings 
            WHERE status = "BORROWED" AND due_date < CURRENT_TIMESTAMP
        ''')
        stats['overdue_books'] = cursor.fetchone()['count']
        
        # Total transactions
        cursor.execute('SELECT COUNT(*) as count FROM transactions')
        stats['total_transactions'] = cursor.fetchone()['count']
        
        # Books by category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM books 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        stats['books_by_category'] = [dict(row) for row in cursor.fetchall()]
        
        # Most borrowed books
        cursor.execute('''
            SELECT b.title, b.author, COUNT(*) as borrow_count
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            WHERE t.transaction_type = 'BORROW'
            GROUP BY t.book_id
            ORDER BY borrow_count DESC
            LIMIT 10
        ''')
        stats['most_borrowed'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return stats
        
    def get_book_borrowing_count(self, book_id: str) -> int:
        """Get how many times a book has been borrowed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM transactions 
            WHERE book_id = ? AND transaction_type = 'BORROW'
        ''', (book_id,))
        
        count = cursor.fetchone()['count']
        conn.close()
        return count