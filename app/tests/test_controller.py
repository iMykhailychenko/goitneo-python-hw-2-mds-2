import unittest

from app.controller import controller
from app.models import AddressBook, Phone, Record, Name


class TestController(unittest.TestCase):
    def get_contacts(self):
        contacts = AddressBook()

        record1 = Record("Ivan")
        record1.add_phone("1234567890")

        record2 = Record("Taras")
        record2.add_phone("0987654321")

        contacts.add_contact(record1)
        contacts.add_contact(record2)

        return contacts

    def test_exit_command(self):
        """Returns None for exit or close commands"""
        result = controller("exit", AddressBook())
        self.assertIsNone(result)

        result = controller("close", AddressBook())
        self.assertIsNone(result)

    def test_case_insensitive(self):
        """Handle 'Hello' command in case insensitive manner"""
        result = controller("Hello", AddressBook())
        self.assertEqual(result, "How can I help you?")

        result = controller("HeLLo", AddressBook())
        self.assertEqual(result, "How can I help you?")

        result = controller("hello", AddressBook())
        self.assertEqual(result, "How can I help you?")

    def test_add_command(self):
        """Handle 'add' command"""
        contacts = AddressBook()

        result = controller("add Ivan 1234567890", contacts)
        phones = contacts.data[Name("Ivan")].phones

        self.assertEqual(result, "Contact added.")
        self.assertEqual(phones, {Phone("1234567890")})

        # Test case with second phone number
        result = controller("add Ivan 0987654321", contacts)
        self.assertEqual(result, "Contact added.")
        self.assertEqual(phones, {Phone("1234567890"), Phone("0987654321")})

    def test_change_command(self):
        """Handle 'change' command"""
        contacts = self.get_contacts()

        # Test if original phone is exist
        phones = contacts.data[Name("Ivan")].phones
        self.assertEqual(phones, {Phone("1234567890")})

        result = controller("change Ivan 1234567890 4321954783", contacts)

        # Test if original phone was changed
        self.assertEqual(result, "Contact changed.")
        self.assertEqual(phones, {Phone("4321954783")})

        # Test case for changing non-existent contact
        result = controller("change John 9876543210 1234567890", contacts)
        self.assertEqual(result, "User do not exist.")  # Ensure no changes

    def test_get_contact(self):
        """Handle 'phone' command"""
        contacts = self.get_contacts()

        result = controller("phone Taras", contacts)
        self.assertEqual(result, "Contact name: Taras, phones: 0987654321")

        # Test case for non-existent contact
        result = controller("phone John", contacts)
        self.assertEqual(result, "Contact not found.")

    def test_get_all_contact(self):
        """Handle 'all' command"""
        contacts = self.get_contacts()

        result = controller("all", contacts)
        self.assertEqual(
            result,
            "Contact name: Ivan, phones: 1234567890\nContact name: Taras, phones: 0987654321",
        )

        # Test case for empty contacts
        result = controller("all", AddressBook())
        self.assertEqual(result, "No contacts available.")

    def test_invalid_command(self):
        """Handle invalid command"""
        result = controller("test", AddressBook())
        self.assertEqual(result, "Invalid command.")

        contacts = self.get_contacts()
        result = controller("change Ivan 1234567890", contacts)
        self.assertEqual(result, "Invalid command.")

        result = controller("change Ivan", contacts)
        self.assertEqual(result, "Invalid command.")

    def test_invalid_phone(self):
        """Handle invalid command"""
        result = controller("add Ivan 12345678900", AddressBook())  # Long
        self.assertEqual(result, "Phone number must be 10 digits long.")

        result = controller("add Ivan A234567890", AddressBook())  # Test letter
        self.assertEqual(result, "Phone number must be 10 digits long.")

        result = controller("add Ivan 123456789", AddressBook())
        self.assertEqual(result, "Phone number must be 10 digits long.")  # Short
