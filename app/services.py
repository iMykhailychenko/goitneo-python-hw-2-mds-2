from app.models import AddressBook, Record


def parse_input(user_input: str) -> list[str]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args: list, contacts: AddressBook) -> str:
    name, phone = args

    record = Record(name)
    record.add_phone(phone)

    contacts.add_contact(record)
    return "Contact added."


def change_contact(args: list, contacts: AddressBook) -> str:
    name, old_phone, new_phone = args

    record = contacts.find_contact(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError("User do not exist.")


def get_contact(args: list, contacts: AddressBook) -> str:
    return str(contacts.find_contact(args[0]) or "Contact not found.")


def get_all_contacts(contacts: AddressBook) -> str:
    return str(contacts) or "No contacts available."
