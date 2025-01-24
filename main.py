import psycopg2
from config import get_connection

#function for Admin Login
def librarian_login():
   email = input("Enter Email: ")
   password = input("Enter Password: ")

   try:
       conn = get_connection()
       if conn is None:
           print("Failed to connect to the database.")
           return False

       cur = conn.cursor()
       cur.execute("SELECT librarian_id, password FROM librarians WHERE email = %s", (email,))
       result = cur.fetchone()

       if result and result[1] == password:
           print(f"Login Successful! Librarian ID: {result[0]}")
           return result[0]  # Return librarian ID
       else:
           print("Invalid email or password.")
       
   except psycopg2.Error as e:
       print(f"Database error: {e}")
   finally:
       if conn:
           conn.close()
   
   return False

#function to search Books
def search_books():
   keyword = input("Enter book title or author keyword: ").strip()

   try:
       conn = get_connection()
       if conn is None:
           print("Failed to connect to the database.")
           return

       cur = conn.cursor()
       query = "SELECT book_id, title, author, publication_year, total_copies, available_copies FROM books WHERE title ILIKE %s OR author ILIKE %s"
       cur.execute(query, (f"%{keyword}%", f"%{keyword}%"))
       results = cur.fetchall()

       if results:
           print("\nBooks found:")
           print("ID | Title | Author | Year | Available Copies")
           print("-" * 60)
           for row in results:
               print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[5]}")
       else:
           print("No books found.")

   except psycopg2.Error as e:
       print(f"Database error: {e}")
   finally:
       if conn:
           conn.close()

#function to register student
def register_student():
   name = input("Enter student name: ").strip()
   email = input("Enter student email: ").strip()

   try:
       conn = get_connection()
       if conn is None:
           print("Failed to connect to the database.")
           return

       cur = conn.cursor()
       cur.execute("INSERT INTO students (name, email, status) VALUES (%s, %s, 'pending') RETURNING student_id", (name, email))
       student_id = cur.fetchone()[0]
       conn.commit()

       print(f"Student registered with ID: {student_id}")

   except psycopg2.IntegrityError:
       print("Error: Student with this email already exists.")
   except psycopg2.Error as e:
       print(f"Database error: {e}")
   finally:
       if conn:
           conn.close()

#function to approve or reject student
def approve_student(librarian_id):
    student_id = input("Enter student ID to approve/reject: ").strip()
    status = input("Enter 'approve' or 'reject': ").lower().strip()
    document_verified = input("Is document verified? (yes/no): ").lower().strip() == 'yes'

    if status not in ("approve", "reject"):
        print("Invalid status. Please enter 'approve' or 'reject'.")
        return

    try:
        conn = get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return

        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET status = %s, approved_by = %s, document_verified = %s WHERE student_id = %s",
            (status, librarian_id, document_verified, student_id)
        )
        
        if cur.rowcount == 0:
            print(f"No student found with ID {student_id}.")
        else:
            conn.commit()
            print(f"Student {status}d successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

#function to add Books
def add_book():
   title = input("Enter book title: ").strip()
   author = input("Enter author name: ").strip()
   
   while True:
       try:
           year = int(input("Enter published year: "))
           total_copies = int(input("Enter total copies: "))
           break
       except ValueError:
           print("Please enter valid numeric values.")

   try:
       conn = get_connection()
       if conn is None:
           print("Failed to connect to the database.")
           return

       cur = conn.cursor()
       cur.execute(
           "INSERT INTO books (title, author, publication_year, total_copies, available_copies) VALUES (%s, %s, %s, %s, %s)",
           (title, author, year, total_copies, total_copies)
       )
       conn.commit()

       print("Book added successfully!")

   except psycopg2.Error as e:
       print(f"Database error: {e}")
   finally:
       if conn:
           conn.close()

#function to issue a book
def issue_book(student_id):
    book_id = input("Enter book ID to issue: ").strip()

    try:
        conn = get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return

        cur = conn.cursor()
        
        # Check if book is available
        cur.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
        book = cur.fetchone()
        
        if not book or book[0] <= 0:
            print("Book not available for issuing.")
            return

        # Check student status
        cur.execute("SELECT status FROM students WHERE student_id = %s", (student_id,))
        student = cur.fetchone()
        
        if not student or student[0] != 'approve':
            print("Student not approved to borrow books.")
            return

        # Issue book
        cur.execute(
            "INSERT INTO book_issues (student_id, book_id, issue_date) VALUES (%s, %s, CURRENT_DATE)",
            (student_id, book_id)
        )
        
        # Update book available copies
        cur.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s",
            (book_id,)
        )
        
        conn.commit()
        print(f"Book {book_id} issued to student {student_id} successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

#funtion to return book
def return_book(student_id):
    book_id = input("Enter book ID to return: ").strip()

    try:
        conn = get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return

        cur = conn.cursor()
        
        # Check if book was issued to this student
        cur.execute(
            "SELECT issue_id FROM book_issues WHERE student_id = %s AND book_id = %s AND return_date IS NULL",
            (student_id, book_id)
        )
        issue = cur.fetchone()
        
        if not issue:
            print("No active issue found for this book.")
            return

        # Return book
        cur.execute(
            "UPDATE book_issues SET return_date = CURRENT_DATE WHERE issue_id = %s",
            (issue[0],)
        )
        
        # Update book available copies
        cur.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s",
            (book_id,)
        )
        
        conn.commit()
        print(f"Book {book_id} returned successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()



def main():
    librarian_id = None
    student_id = None
    while True:
        print("\n==== Library Management System ====")
        print("1. Librarian Login")
        print("2. Search Books")
        print("3. Register Student")
        print("4. Approve/Reject Student")
        print("5. Add Book")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            librarian_id = librarian_login()
        elif choice == '2':
            search_books()
        elif choice == '3':
            register_student()
        elif choice == '4':
            if not librarian_id:
                librarian_id = librarian_login()
            if librarian_id:
                approve_student(librarian_id)
        elif choice == '5':
            add_book()
        elif choice == '6':
            if not student_id:
                student_id = input("Enter Student ID: ").strip()
            issue_book(student_id)
        elif choice == '7':
            if not student_id:
                student_id = input("Enter Student ID: ").strip()
            return_book(student_id)
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
   main()