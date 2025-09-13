import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Employee:
    """Class to represent an Employee"""
    def __init__(self, emp_id, name, department, salary, contact, email):
        # Convert everything to string for consistency
        self.emp_id = str(emp_id)
        self.name = str(name)
        self.department = str(department)
        self.salary = str(salary)
        self.contact = str(contact)
        self.email = str(email)

    def __str__(self):
        return (
            f"ID        : {self.emp_id}\n"
            f"Name      : {self.name}\n"
            f"Department: {self.department}\n"
            f"Salary    : {self.salary}\n"
            f"Contact   : {self.contact}\n"
            f"Email     : {self.email}\n"
            "--------------------------"
        )


class EmailSender:
    """A class responsible for sending emails"""
    def __init__(self, sender_email, sender_password):
        self.sender_email = str(sender_email)
        self.sender_password = str(sender_password)

    def send_email(self, employee_name, employee_email, email_subject, email_body):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = str(employee_email)
        msg["Subject"] = str(email_subject)
        msg.attach(MIMEText(str(email_body), "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, str(employee_email), msg.as_string())
            server.quit()
            print(f"📧 Email successfully sent to {employee_name} ({employee_email}).")
        except Exception as e:
            print("❌ Email not sent.")
            print(e)


class EmployeeManagementSystem:
    """Class to manage employees"""
    def __init__(self, email_sender):
        self.employees = []
        self.email_sender = email_sender

    def add_employee(self):
        print("\n--- Add Employee ---")
        emp_id = str(input("Enter Employee ID: "))

        if any(emp.emp_id == emp_id for emp in self.employees):
            print("❌ Error: Employee ID already exists.\n")
            return

        name = str(input("Enter Employee Name: "))
        department = str(input("Enter Employee Department: "))
        salary = str(input("Enter Employee Salary: "))
        contact = str(input("Enter Employee Contact: "))
        email = str(input("Enter Employee Email: "))

        new_emp = Employee(emp_id, name, department, salary, contact, email)
        self.employees.append(new_emp)
        print("✅ Employee added successfully.\n")

        # Send confirmation email
        subject = "Welcome to the Company!"
        body = (
            f"Dear {name},\n\n"
            f"Welcome to the {department} department! 🎉\n"
            f"Your Employee ID is {emp_id}.\n\n"
            "We are excited to have you onboard.\n\n"
            "Best Regards,\nHR Team"
        )
        self.email_sender.send_email(name, email, subject, body)

    def view_employee(self):
        print("\n--- View Employee ---")
        emp_id = str(input("Enter Employee ID to view: "))
        for emp in self.employees:
            if emp.emp_id == emp_id:
                print(emp)
                return
        print("❌ Employee not found.\n")

    def update_employee(self):
        print("\n--- Update Employee ---")
        emp_id = str(input("Enter Employee ID to update: "))
        for emp in self.employees:
            if emp.emp_id == emp_id:
                emp.name = str(input(f"Enter new name ({emp.name}): ") or emp.name)
                emp.department = str(input(f"Enter new department ({emp.department}): ") or emp.department)
                emp.salary = str(input(f"Enter new salary ({emp.salary}): ") or emp.salary)
                emp.contact = str(input(f"Enter new contact ({emp.contact}): ") or emp.contact)
                emp.email = str(input(f"Enter new email ({emp.email}): ") or emp.email)
                print("✅ Employee updated successfully.\n")
                return
        print("❌ Employee not found.\n")

    def delete_employee(self):
        print("\n--- Delete Employee ---")
        emp_id = str(input("Enter Employee ID to delete: "))
        for emp in self.employees:
            if emp.emp_id == emp_id:
                confirm = str(input(f"Are you sure you want to delete {emp.name}? (yes/no): ")).strip().lower()
                if confirm == "yes":
                    self.employees.remove(emp)
                    print("✅ Employee deleted successfully.\n")
                else:
                    print("❌ Deletion aborted.\n")
                return
        print("❌ Employee not found.\n")

    def list_employees(self):
        print("\n--- Employee List ---")
        if not self.employees:
            print("No employees found.\n")
            return
        for emp in self.employees:
            print(emp)

    def department_wide_report(self):
        print("\n--- Department Wide Report ---")
        if not self.employees:
            print("No employees found.\n")
            return

        dept_dict = {}
        for emp in self.employees:
            dept_dict.setdefault(emp.department, []).append(emp)

        print("Available Departments:")
        for dept in dept_dict.keys():
            print(f"- {dept}")

        selected_dept = str(input("\nEnter the department you want to view: ")).strip()
        matching_depts = [d for d in dept_dict if d.lower() == selected_dept.lower()]
        if not matching_depts:
            print(f"❌ Error: Department '{selected_dept}' does not exist.\n")
            return

        selected_dept = matching_depts[0]
        print(f"\nEmployees in Department: {selected_dept}")
        print("------------------------------------------------------------")
        print(f"{'ID':<10}{'Name':<20}{'Department':<15}{'Salary':<12}{'Contact'}")
        print("------------------------------------------------------------")
        for emp in dept_dict[selected_dept]:
            print(f"{emp.emp_id:<10}{emp.name:<20}{emp.department:<15}{emp.salary:<12}{emp.contact}")
        print("------------------------------------------------------------\n")

    def main_menu(self):
        while True:
            print("\n===== Employee Management System =====")
            print("1. Add Employee")
            print("2. View Employee")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. List All Employees")
            print("6. Department Wide Report")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.view_employee()
            elif choice == "3":
                self.update_employee()
            elif choice == "4":
                self.delete_employee()
            elif choice == "5":
                self.list_employees()
            elif choice == "6":
                self.department_wide_report()
            elif choice == "7":
                print("Exiting system. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Try again.")


# Start the program
if __name__ == "__main__":
    EMAIL_ADDRESS = "razigani@gmail.com"
    EMAIL_PASSWORD = "jhpx tfif unlk crgy"  # App password

    email_sender = EmailSender(EMAIL_ADDRESS, EMAIL_PASSWORD)
    ems = EmployeeManagementSystem(email_sender)
    ems.main_menu()
