# Library Management System

## Overview
This Library Management System is a comprehensive Python-based application that provides a command-line interface for managing library operations. The system supports multiple functionalities for librarians and students, ensuring efficient book management and user tracking.

## Database Configuration
The project uses PostgreSQL as the backend database, with connection details managed in `config.py`. The database name is `library_management`, and it connects to a local PostgreSQL server.

## Features

### 1. Librarian Functions
- **Librarian Login**: Secure authentication for library staff
- **Student Registration Management**
  - Register new students
  - Approve or reject student registrations
  - Verify student documents
- **Book Management**
  - Add new books to the library inventory
  - Search books by title or author
  - Track book availability

### 2. Student Functions
- **Book Searching**
  - Search books using keywords
  - View book details including availability
- **Book Borrowing**
  - Issue books to approved students
  - Return books
  - Track book lending history

## System Workflow

### Login and Access
1. Users start by selecting their desired action from the main menu
2. Librarians must log in to access administrative functions
3. Students can search books without authentication

### Student Registration Process
- Students provide name and email during registration
- Registration status is initially set to 'pending'
- Librarian reviews and approves/rejects registration
- Approved students can borrow books

### Book Management
- Librarians can add new books to the system
- Each book tracks:
  - Total copies
  - Available copies
  - Publication details

### Book Borrowing Flow
- Only approved students can borrow books
- System checks book availability before issuing
- Tracks issue and return dates
- Updates available copies automatically

## Technical Details
- **Language**: Python
- **Database**: PostgreSQL
- **Database Library**: psycopg2
- **Authentication**: Simple password-based

## Setup Requirements
1. Python 3.x
2. PostgreSQL
3. psycopg2 library
4. Create database and tables as per project schema

## Potential Improvements
- Implement password hashing
- Add more robust error handling
- Create a web or GUI interface
- Implement late fee tracking
- Add more detailed reporting

## Disclaimer
Ensure to replace database credentials in `config.py` with your actual database connection details.
