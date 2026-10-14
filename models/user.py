"""
User Model - Represents a library member
"""

import uuid
from datetime import datetime


class User:
    """User entity with borrowing information"""
    
    def __init__(self, name: str, email: str, phone: str):
        self.user_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []  # List of book IDs
        self.borrowing_history = []  # List of transaction IDs
        self.member_since = datetime.now().isoformat()
        self.is_active = True
        
    def to_dict(self):
        """Convert User object to dictionary for JSON storage"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'borrowed_books': self.borrowed_books,
            'borrowing_history': self.borrowing_history,
            'member_since': self.member_since,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User object from dictionary (JSON load)"""
        user = cls(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        user.user_id = data['user_id']
        user.borrowed_books = data.get('borrowed_books', [])
        user.borrowing_history = data.get('borrowing_history', [])
        user.member_since = data.get('member_since', datetime.now().isoformat())
        user.is_active = data.get('is_active', True)
        return user
    
    def borrow_book(self, book_id: str):
        """Add book to borrowed list"""
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
    
    def return_book(self, book_id: str):
        """Remove book from borrowed list"""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
    
    def __str__(self):
        return f"{self.name} ({self.email}) - Borrowed: {len(self.borrowed_books)} books"