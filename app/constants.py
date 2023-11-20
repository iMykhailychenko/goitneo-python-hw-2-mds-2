from enum import Enum


class BotCommands(Enum):
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    HELLO = "hello"
    EXIT = "exit"
    CLOSE = "close"


class InvalidNameError(Exception):
    ...


class InvalidPhoneError(Exception):
    ...
