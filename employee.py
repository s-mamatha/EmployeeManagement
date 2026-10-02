import sqlite3
from database import get_connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT,
            job_role TEXT,
            salary REAL,
            joining_date TEXT
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def add_employee():
    print("\n===== Add Employee =====")

    name = input("Enter employee name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    department = input("Enter department: ").strip()
    job_role = input("Enter job role: ").strip()

    try:
        salary = float(input("Enter salary: "))
    except ValueError:
        print("Please enter a valid salary.")
        return

    joining_date = input("Enter joining date (YYYY-MM-DD): ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO employees
        (name, email, phone, department, job_role, salary, joining_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    values = (
        name,
        email,
        phone,
        department,
        job_role,
        salary,
        joining_date
    )

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Employee added successfully!")

    except sqlite3.IntegrityError:
        connection.rollback()
        print("Email already exists. Please use a different email.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def view_employees():
    print("\n===== Employee List =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            name,
            email,
            phone,
            department,
            job_role,
            salary,
            joining_date
        FROM employees
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    if not employees:
        print("No employees found.")
    else:
        for employee in employees:
            print("----------------------------------------")
            print("Employee ID :", employee[0])
            print("Name        :", employee[1])
            print("Email       :", employee[2])
            print("Phone       :", employee[3])
            print("Department  :", employee[4])
            print("Job Role    :", employee[5])
            print("Salary      :", employee[6])
            print("Joining Date:", employee[7])

    cursor.close()
    connection.close()


def search_employee():
    print("\n===== Search Employee =====")
    print("1. Search by Employee ID")
    print("2. Search by Name")

    choice = input("Enter your choice: ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if choice == "1":
            try:
                employee_id = int(input("Enter employee ID: "))
            except ValueError:
                print("Please enter a valid employee ID.")
                return

            cursor.execute("""
                SELECT
                    employee_id,
                    name,
                    email,
                    phone,
                    department,
                    job_role,
                    salary,
                    joining_date
                FROM employees
                WHERE employee_id = ?
            """, (employee_id,))

        elif choice == "2":
            name = input("Enter employee name: ").strip()

            cursor.execute("""
                SELECT
                    employee_id,
                    name,
                    email,
                    phone,
                    department,
                    job_role,
                    salary,
                    joining_date
                FROM employees
                WHERE name LIKE ?
            """, (f"%{name}%",))

        else:
            print("Invalid choice.")
            return

        employees = cursor.fetchall()

        if not employees:
            print("No employee found.")
        else:
            for employee in employees:
                print("----------------------------------------")
                print("Employee ID :", employee[0])
                print("Name        :", employee[1])
                print("Email       :", employee[2])
                print("Phone       :", employee[3])
                print("Department  :", employee[4])
                print("Job Role    :", employee[5])
                print("Salary      :", employee[6])
                print("Joining Date:", employee[7])

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def update_employee():
    print("\n===== Update Employee =====")

    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Please enter a valid employee ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        print("Employee not found.")
        cursor.close()
        connection.close()
        return

    print("\nEnter new details:")

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    department = input("Enter department: ").strip()
    job_role = input("Enter job role: ").strip()

    try:
        salary = float(input("Enter salary: "))
    except ValueError:
        print("Please enter a valid salary.")
        cursor.close()
        connection.close()
        return

    joining_date = input("Enter joining date (YYYY-MM-DD): ").strip()

    try:
        cursor.execute("""
            UPDATE employees
            SET name = ?,
                email = ?,
                phone = ?,
                department = ?,
                job_role = ?,
                salary = ?,
                joining_date = ?
            WHERE employee_id = ?
        """, (
            name,
            email,
            phone,
            department,
            job_role,
            salary,
            joining_date,
            employee_id
        ))

        connection.commit()
        print("Employee updated successfully!")

    except sqlite3.IntegrityError:
        connection.rollback()
        print("Email already exists. Please use a different email.")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        connection.close()


def delete_employee():
    print("\n===== Delete Employee =====")

    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Please enter a valid employee ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        print("Employee not found.")
        cursor.close()
        connection.close()
        return

    print("Employee found:", employee[0])

    confirmation = input(
        "Are you sure you want to delete this employee? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        cursor.execute(
            "DELETE FROM employees WHERE employee_id = ?",
            (employee_id,)
        )

        connection.commit()
        print("Employee deleted successfully!")
    else:
        print("Delete cancelled.")

    cursor.close()
    connection.close()


def employee_report():
    print("\n===== Employee Report =====")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(salary) FROM employees")
    average_salary = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(salary) FROM employees")
    highest_salary = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(salary) FROM employees")
    lowest_salary = cursor.fetchone()[0]

    print("Total Employees :", total_employees)

    if average_salary is not None:
        print("Average Salary  :", round(average_salary, 2))
        print("Highest Salary  :", highest_salary)
        print("Lowest Salary   :", lowest_salary)
    else:
        print("No salary data available.")

    cursor.close()
    connection.close()