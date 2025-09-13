# test_pdwd_pfs_a03.py
import unittest
from unittest.mock import patch, MagicMock
from pdwd_pfs_a03 import Employee, EmailSender, EmployeeManagementSystem


class TestEmployee(unittest.TestCase):
    def test_employee_str_fields_are_strings(self):
        emp = Employee("E001", "Alice", "HR", 5000, 123456789, "alice@example.com")
        # Check all attributes are strings
        self.assertIsInstance(emp.emp_id, str)
        self.assertIsInstance(emp.name, str)
        self.assertIsInstance(emp.department, str)
        self.assertIsInstance(emp.salary, str)
        self.assertIsInstance(emp.contact, str)
        self.assertIsInstance(emp.email, str)

    def test_employee_str_representation(self):
        emp = Employee("E001", "Alice", "HR", "5000", "123456789", "alice@example.com")
        result = str(emp)
        self.assertIn("Alice", result)
        self.assertIn("HR", result)
        self.assertIn("5000", result)


class TestEmailSender(unittest.TestCase):
    @patch("smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        sender = EmailSender("test@example.com", "password")
        sender.send_email("Alice", "alice@example.com", "Test Subject", "Hello!")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with("test@example.com", "password")
        mock_server.sendmail.assert_called_once()


class TestEmployeeManagementSystem(unittest.TestCase):
    def setUp(self):
        self.mock_email_sender = MagicMock()
        self.ems = EmployeeManagementSystem(self.mock_email_sender)

    @patch("builtins.input", side_effect=["E001", "Alice", "HR", "5000", "123456789", "alice@example.com"])
    def test_add_employee(self, mock_input):
        self.ems.add_employee()
        self.assertEqual(len(self.ems.employees), 1)
        emp = self.ems.employees[0]
        self.assertEqual(emp.name, "Alice")
        # Assert all fields are strings
        self.assertTrue(all(isinstance(value, str) for value in vars(emp).values()))

    @patch("builtins.input", side_effect=["E001"])
    def test_view_employee_found(self, mock_input):
        self.ems.employees.append(Employee("E001", "Alice", "HR", "5000", "123456789", "alice@example.com"))
        with patch("builtins.print") as mock_print:
            self.ems.view_employee()
            mock_print.assert_any_call(self.ems.employees[0])

    @patch("builtins.input", side_effect=["E002"])
    def test_view_employee_not_found(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.ems.view_employee()
            mock_print.assert_any_call("❌ Employee not found.\n")

    @patch("builtins.input", side_effect=["E001"])
    def test_delete_employee_not_found(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.ems.delete_employee()
            mock_print.assert_any_call("❌ Employee not found.\n")

    def test_list_employees_empty(self):
        with patch("builtins.print") as mock_print:
            self.ems.list_employees()
            mock_print.assert_any_call("No employees found.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)

