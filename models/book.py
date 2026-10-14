"""
Book Model - Represents a book in the library
"""

import uuid
from datetime import datetime


class Book:
    """Book entity with all its attributes"""
    
    def __init__(self, title: str, author: str, isbn: str, 
                 category: str, total_copies: int = 1):
        self.book_id = str(uuid.uuid4())[:8]  # Generate unique ID
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.borrowed_by = []  # List of user IDs
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
    def to_dict(self):
        """Convert Book object to dictionary for JSON storage"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'borrowed_by': self.borrowed_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Book object from dictionary (JSON load)"""
        book = cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            category=data['category'],
            total_copies=data['total_copies']
        )
        book.book_id = data['book_id']
        book.available_copies = data['available_copies']
        book.borrowed_by = data.get('borrowed_by', [])
        book.created_at = data.get('created_at', datetime.now().isoformat())
        book.updated_at = data.get('updated_at', datetime.now().isoformat())
        return book
    
    def update_availability(self, change: int):
        """Update available copies (positive for add, negative for remove)"""
        self.available_copies += change
        self.updated_at = datetime.now().isoformat()
        
    def is_available(self) -> bool:
        """Check if book has available copies"""
        return self.available_copies > 0
    
    def __str__(self):
        return f"{self.title} by {self.author} (Available: {self.available_copies}/{self.total_copies})"