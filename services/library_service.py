"""
Library Service - Core business logic
"""

from typing import List, Dict, Optional
from database.db_manager import DatabaseManager


class LibraryService:
    """Main service class for library operations"""
    
    def __init__(self):
        self.db = DatabaseManager()
        
    # ============ BOOK OPERATIONS ============
    
    def add_book(self, title: str, author: str, isbn: str, 
                 category: str, total_copies: int = 1) -> Optional[str]:
        """Add a new book"""
        if not all([title, author, isbn, category]):
            print("Error: All fields are required")
            return None
            
        if total_copies < 1:
            print("Error: Total copies must be at least 1")
            return None
            
        return self.db.add_book(title, author, isbn, category, total_copies)
        
    def get_all_books(self) -> List[Dict]:
        return self.db.get_all_books()
        
    def search_books(self, keyword: str) -> List[Dict]:
        if not keyword:
            return self.get_all_books()
        return self.db.search_books(keyword)
        
    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        return self.db.get_book_by_id(book_id)
        
    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        return self.db.get_book_by_isbn(isbn)
        
    def update_book(self, book_id: str, **kwargs) -> bool:
        return self.db.update_book(book_id, **kwargs)
        
    def delete_book(self, book_id: str) -> bool:
        return self.db.delete_book(book_id)
        
    def get_books_by_category(self, category: str) -> List[Dict]:
        return self.db.get_books_by_category(category)
        
    def is_book_available(self, book_id: str) -> bool:
        return self.db.is_book_available(book_id)
        
    # ============ USER OPERATIONS ============
    
    def add_user(self, name: str, email: str, phone: str) -> Optional[str]:
        if not all([name, email, phone]):
            print("Error: All fields are required")
            return None
        return self.db.add_user(name, email, phone)
        
    def get_all_users(self) -> List[Dict]:
        return self.db.get_all_users()
        
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        return self.db.get_user_by_id(user_id)
        
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.db.get_user_by_email(email)
        
    def update_user(self, user_id: str, **kwargs) -> bool:
        return self.db.update_user(user_id, **kwargs)
        
    def delete_user(self, user_id: str) -> bool:
        return self.db.delete_user(user_id)
        
    # ============ BORROWING OPERATIONS ============
    
    def borrow_book(self, user_id: str, book_id: str) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            print("Error: User not found")
            return False
            
        book = self.get_book_by_id(book_id)
        if not book:
            print("Error: Book not found")
            return False
            
        if not self.is_book_available(book_id):
            print("Error: Book is not available")
            return False
            
        return self.db.borrow_book(user_id, book_id)
        
    def return_book(self, user_id: str, book_id: str) -> bool:
        return self.db.return_book(user_id, book_id)
        
    def get_current_borrowings(self) -> List[Dict]:
        return self.db.get_current_borrowings()
        
    def get_overdue_books(self) -> List[Dict]:
        return self.db.get_overdue_books()
        
    # ============ TRANSACTION HISTORY ============
    
    def get_transaction_history(self, user_id: Optional[str] = None, 
                                limit: int = 50) -> List[Dict]:
        return self.db.get_transaction_history(user_id, limit)
        
    def get_user_borrowing_history(self, user_id: str) -> List[Dict]:
        return self.db.get_user_borrowing_history(user_id)
        
    # ============ STATISTICS ============
    
    def get_statistics(self) -> Dict:
        return self.db.get_statistics()
        
    def get_book_borrowing_count(self, book_id: str) -> int:
        return self.db.get_book_borrowing_count(book_id)