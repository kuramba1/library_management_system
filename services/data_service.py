"""
Data Service - Handles data persistence (JSON file storage)
"""

import json
import os
from typing import Dict, List, Optional
from models.book import Book
from models.user import User
from models.transaction import Transaction


class DataService:
    """Handles all data storage operations"""
    
    def __init__(self, data_file: str = 'data/library_data.json'):
        self.data_file = data_file
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
    def save_data(self, books: Dict[str, Book], users: Dict[str, User], 
                  transactions: List[Transaction]):
        """Save all data to JSON file"""
        data = {
            'books': {book_id: book.to_dict() for book_id, book in books.items()},
            'users': {user_id: user.to_dict() for user_id, user in users.items()},
            'transactions': [t.to_dict() for t in transactions]
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
            
    def load_data(self):
        """Load data from JSON file"""
        if not os.path.exists(self.data_file):
            return {}, {}, []  # Empty data
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Convert dictionaries back to objects
            books = {}
            for book_id, book_data in data.get('books', {}).items():
                books[book_id] = Book.from_dict(book_data)
                
            users = {}
            for user_id, user_data in data.get('users', {}).items():
                users[user_id] = User.from_dict(user_data)
                
            transactions = []
            for trans_data in data.get('transactions', []):
                transactions.append(Transaction.from_dict(trans_data))
                
            return books, users, transactions
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}, {}, []