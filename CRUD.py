import psycopg2
from psycopg2 import Error

# Import database login info from config.py
try:
    from config import DB_CONFIG
except ImportError:
    print("Fail to load config.py")
    exit(1)

# Connect to data base
def connect_db():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

# Fetch and print all students
def getAllStudents():
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
        students = cur.fetchall()

        for s in students:
            print(f"ID: {s[0]} | Name: {s[1]} {s[2]} | Email: {s[3]} | Enrollment Date: {s[4]}")
        print("\n")

    except Error as e:
        print("Fail to fetch students", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Insert new student
def addStudent(first_name, last_name, email, enrollment_date):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()

        sql = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);"
        cur.execute(sql, (first_name, last_name, email, enrollment_date))

        conn.commit()
        print(f"Successfully added student: {first_name} {last_name}\n")

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Fail to add student", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Update student email with ID
def updateStudentEmail(student_id, new_email):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()

        sql = "UPDATE students SET email = %s WHERE student_id = %s;"
        cur.execute(sql, (new_email, student_id))

        # Check if any row was updated
        if cur.rowcount == 0:
            print(f"No student found with ID {student_id}.\n")
        else:
            conn.commit()
            print(f"Successfully updated email for student ID {student_id}.\n")

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Database error while updating email:", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Remove student with ID
def deleteStudent(student_id):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()

        sql = "DELETE FROM students WHERE student_id = %s;"
        cur.execute(sql, (student_id,))

        if cur.rowcount == 0:
            print(f"No student found with ID {student_id}.\n")
        else:
            conn.commit()
            print(f"Successfully deleted student ID {student_id}.\n")

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Fail to delete student", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def main():
    # Menu
    while True:
        print("1. Get all students")
        print("2. Add a student")
        print("3. Update student email")
        print("4. Delete a student")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            email = input("Enter email: ").strip()
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == "3":
            try:
                student_id = int(input("Enter student ID: ").strip())
                new_email = input("Enter new email: ").strip()
                updateStudentEmail(student_id, new_email)
            except ValueError:
                print("Invalid input. Student ID must be an integer.\n")
        elif choice == "4":
            try:
                student_id = int(input("Enter student ID to delete: ").strip())
                deleteStudent(student_id)
            except ValueError:
                print("Invalid input. Student ID must be an integer.\n")
        elif choice == "5":
            print("Exit successfully!")
            break
        else:
            print("Invalid choice, please follow the instruction.\n")


if __name__ == "__main__":
    main()