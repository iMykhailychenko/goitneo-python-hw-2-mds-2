from collections import UserDict
from typing import Optional

from app.constants import InvalidNameError, InvalidPhoneError


class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Field) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not isinstance(other, Field) or self.value != other.value

    def __hash__(self) -> int:
        return hash(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        if not value:
            raise InvalidNameError()

        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        if len(value) != 10:
            raise InvalidPhoneError()
        elif not value.isnumeric():
            raise InvalidPhoneError()

        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: set[Phone] = set()

    def __str__(self) -> str:
        return f"Contact name: {self.name}, phones: {'; '.join(map(str, self.phones))}"

    def add_phone(self, phone: str) -> None:
        self.phones.add(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones.discard(Phone(phone))

    def edit_phone(
        self,
        old_phone: str,
        new_phone: str,
    ) -> None:
        self.phones.discard(Phone(old_phone))
        self.phones.add(Phone(new_phone))

    def find_phone(self, query: str) -> Phone:
        return [phone for phone in self.phones if phone.value.lower() in query.lower()]


class AddressBook(UserDict[Name, Record]):
    def __str__(self) -> str:
        return "\n".join(str(contact) for contact in self.data.values())

    def add_contact(self, contact: Record) -> None:
        name = contact.name
        phones = contact.phones

        if self.data.get(name):
            for phone in phones:
                self.data[name].add_phone(phone.value)
        else:
            self.data[name] = contact

    def find_contact(self, name: str) -> Optional[Record]:
        return self.data.get(Name(name), None)
