from enum import Enum, auto


class State(Enum):
    FIRST_NODE = auto()
    REVIEW = auto()
    HELP_CHOSE_SUBJECT = auto()
    HELP_CHOSE_SUBJECT_OTHER = auto()
    HELP_CHOSE_TYPE = auto()
    HELP_CHOSE_AWARD = auto()
    HELP_MATCHING = auto()
    HELP_MATCHED = auto()
    ADD_T = auto()
    READ_T = auto()