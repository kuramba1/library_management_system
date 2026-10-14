"""
Transaction Model - Records all borrow/return operations
"""

import uuid
from datetime import datetime


class Transaction:
    """Transaction entity for tracking operations"""
    
    def __init__(self, book_id: str, user_id: str, transaction_type: str):
        self.transaction_id = str(uuid.uuid4())[:8]
        self.book_id = book_id
        self.user_id = user_id
        self.transaction_type = transaction_type  # 'BORROW' or 'RETURN'
        self.timestamp = datetime.now().isoformat()
        self.status = 'COMPLETED'
        
    def to_dict(self):
        """Convert Transaction object to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'timestamp': self.timestamp,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Transaction object from dictionary"""
        transaction = cls(
            book_id=data['book_id'],
            user_id=data['user_id'],
            transaction_type=data['transaction_type']
        )
        transaction.transaction_id = data['transaction_id']
        transaction.timestamp = data.get('timestamp', datetime.now().isoformat())
        transaction.status = data.get('status', 'COMPLETED')
        return transaction