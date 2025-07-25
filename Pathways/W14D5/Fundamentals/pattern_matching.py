"""
Library Management System
A system to manage books, members, and borrowing records.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class Book:
    def __init__(self, isbn: str, title: str, author: str, genre: str, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by: List[str] = []

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def is_available(self) -> bool:
        return self.available_copies > 0


class Member:
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books: List[str] = []
        self.borrowing_history: List[Dict] = []
        self.membership_start = datetime.now()

    def can_borrow(self, max_books: int = 5) -> bool:
        return len(self.borrowed_books) < max_books

    def __str__(self) -> str:
        return f"Member {self.name} (ID: {self.member_id})"


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.borrowing_records: List[Dict] = []

    def add_book(self, book: Book) -> bool:
        """Add a book to the library catalog."""
        if book.isbn in self.books:
            # Book already exists, increase copies
            self.books[book.isbn].total_copies += book.total_copies
            self.books[book.isbn].available_copies += book.available_copies
            return True
        else:
            self.books[book.isbn] = book
            return True

    def register_member(self, member: Member) -> bool:
        """Register a new member."""
        if member.member_id in self.members:
            return False
        self.members[member.member_id] = member
        return True

    def borrow_book(self, member_id: str, isbn: str) -> Optional[str]:
        """Process a book borrowing request."""
        if member_id not in self.members:
            return "Member not found"
        
        if isbn not in self.books:
            return "Book not found"
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if not member.can_borrow():
            return "Member has reached borrowing limit"
        
        if not book.is_available():
            return "Book not available"
        
        # Process the borrowing
        book.available_copies -= 1
        book.borrowed_by.append(member_id)
        member.borrowed_books.append(isbn)
        
        # Record the transaction
        borrowing_record = {
            'member_id': member_id,
            'isbn': isbn,
            'borrow_date': datetime.now(),
            'due_date': datetime.now() + timedelta(days=14),
            'returned': False
        }
        
        self.borrowing_records.append(borrowing_record)
        member.borrowing_history.append(borrowing_record)
        
        return None  # Success

    def return_book(self, member_id: str, isbn: str) -> Optional[str]:
        """Process a book return."""
        if member_id not in self.members:
            return "Member not found"
        
        if isbn not in self.books:
            return "Book not found"
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if isbn not in member.borrowed_books:
            return "Book not borrowed by this member"
        
        # Process the return
        book.available_copies += 1
        book.borrowed_by.remove(member_id)
        member.borrowed_books.remove(isbn)
        
        # Update borrowing record
        for record in self.borrowing_records:
            if (record['member_id'] == member_id and 
                record['isbn'] == isbn and 
                not record['returned']):
                record['returned'] = True
                record['return_date'] = datetime.now()
                break
        
        return None  # Success

    def get_overdue_books(self) -> List[Dict]:
        """Get list of overdue books."""
        overdue = []
        current_date = datetime.now()
        
        for record in self.borrowing_records:
            if not record['returned'] and record['due_date'] < current_date:
                overdue.append(record)
        
        return overdue

    def search_books(self, query: str) -> List[Book]:
        """Search for books by title or author."""
        results = []
        query_lower = query.lower()
        
        for book in self.books.values():
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower()):
                results.append(book)
        
        return results

    def generate_report(self) -> Dict:
        """Generate a library usage report."""
        total_books = sum(book.total_copies for book in self.books.values())
        total_borrowed = sum(len(book.borrowed_by) for book in self.books.values())
        total_members = len(self.members)
        
        overdue_count = len(self.get_overdue_books())
        
        return {
            'total_books': total_books,
            'total_borrowed': total_borrowed,
            'total_members': total_members,
            'overdue_count': overdue_count,
            'utilization_rate': (total_borrowed / total_books) * 100 if total_books > 0 else 0
        }

    def save_to_file(self, filename: str) -> bool:
        """Save library data to JSON file."""
        try:
            data = {
                'name': self.name,
                'books': {isbn: {
                    'title': book.title,
                    'author': book.author,
                    'genre': book.genre,
                    'total_copies': book.total_copies,
                    'available_copies': book.available_copies
                } for isbn, book in self.books.items()},
                'members': {mid: {
                    'name': member.name,
                    'email': member.email,
                    'phone': member.phone,
                    'borrowed_books': member.borrowed_books
                } for mid, member in self.members.items()}
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False


def main():
    """Example usage of the library system."""
    # Create library
    library = Library("City Central Library")
    
    # Add some books
    books = [
        Book("978-0-7432-7356-5", "To Kill a Mockingbird", "Harper Lee", "Fiction", 3),
        Book("978-0-385-33312-0", "The Da Vinci Code", "Dan Brown", "Thriller", 2),
        Book("978-0-06-112008-4", "The Alchemist", "Paulo Coelho", "Philosophy", 4)
    ]
    
    for book in books:
        library.add_book(book)
    
    # Register members
    members = [
        Member("M001", "Alice Johnson", "alice@email.com", "555-0101"),
        Member("M002", "Bob Smith", "bob@email.com", "555-0102"),
        Member("M003", "Carol Williams", "carol@email.com", "555-0103")
    ]
    
    for member in members:
        library.register_member(member)
    
    # Simulate some borrowing
    library.borrow_book("M001", "978-0-7432-7356-5")
    library.borrow_book("M002", "978-0-385-33312-0")
    
    # Generate and print report
    report = library.generate_report()
    print(f"Library Report for {library.name}:")
    print(f"Total books: {report['total_books']}")
    print(f"Books borrowed: {report['total_borrowed']}")
    print(f"Total members: {report['total_members']}")
    print(f"Utilization rate: {report['utilization_rate']:.1f}%")
    
    # Save library data
    success = library.save_to_file("library_data.json")
    if success:  
        print("Library data saved successfully!")
    else:
        print("Failed to save library data.")


if __name__ == "__main__":
    main()