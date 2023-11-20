from typing import Union

from app.constants import BotCommands
from app.models import AddressBook
from app.services import (
    add_contact,
    change_contact,
    get_all_contacts,
    get_contact,
    parse_input,
)
from app.validations import input_error


@input_error
def controller(user_input: str, contacts: AddressBook) -> Union[str, None]:
    cmd, *args = parse_input(user_input)

    if cmd == BotCommands.ADD.value:
        return add_contact(args, contacts)
    elif cmd == BotCommands.CHANGE.value:
        return change_contact(args, contacts)
    elif cmd == BotCommands.PHONE.value:
        return get_contact(args, contacts)
    elif cmd == BotCommands.ALL.value:
        return get_all_contacts(contacts)
    elif cmd == BotCommands.HELLO.value:
        return "How can I help you?"
    elif cmd == BotCommands.EXIT.value or cmd == BotCommands.CLOSE.value:
        return None
    else:
        return "Invalid command."
