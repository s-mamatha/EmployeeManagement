from employee import (
    create_table,
    add_employee,
    view_employees,
    search_employee,
    update_employee,
    delete_employee,
    employee_report
)


create_table()


while True:
    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Employee Report")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        employee_report()

    elif choice == "7":
        print("Thank you for using Employee Management System!")
        break

    else:
        print("Invalid choice. Please try again.")