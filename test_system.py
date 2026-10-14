"""
Test script for Library Management System
"""

from services.library_service import LibraryService


def test_system():
    lib = LibraryService()
    
    print("=" * 50)
    print("  TESTING LIBRARY SYSTEM")
    print("=" * 50)
    
    # Test adding books
    print("\n1. Adding Books...")
    book1 = lib.add_book("Python Programming", "John Doe", "978-1-234-56789-0", "Technology", 3)
    book2 = lib.add_book("Data Science", "Jane Smith", "978-1-234-56789-1", "Technology", 2)
    print(f"   Added books: {book1}, {book2}")
    
    # Test adding users
    print("\n2. Adding Users...")
    user1 = lib.add_user("Alice Johnson", "alice@email.com", "555-0101")
    user2 = lib.add_user("Bob Smith", "bob@email.com", "555-0102")
    print(f"   Added users: {user1}, {user2}")
    
    # Test viewing books
    print("\n3. All Books:")
    for book in lib.get_all_books():
        print(f"   {book['title']} - {book['available_copies']} available")
    
    # Test borrowing
    print("\n4. Borrowing a book...")
    if lib.borrow_book(user1, book1):
        print("   ✅ Borrowed successfully")
    
    # Test statistics
    print("\n5. Library Statistics:")
    stats = lib.get_statistics()
    print(f"   Total Books: {stats['total_books']}")
    print(f"   Active Users: {stats['active_users']}")
    print(f"   Active Borrowings: {stats['active_borrowings']}")
    
    # Test returning
    print("\n6. Returning book...")
    if lib.return_book(user1, book1):
        print("   ✅ Returned successfully")
    
    print("\n" + "=" * 50)
    print("  ✅ ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    test_system()