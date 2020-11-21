from enum import Enum, auto


class State(Enum):
    FIRST_NODE = auto()
    REVIEW = auto()
    ADD_T = auto()
    READ_T = auto()

    HELP_CHOSE_SUBJECT = auto()
    HELP_CHOSE_SUBJECT_OTHER = auto()
    HELP_CHOSE_TYPE = auto()
    HELP_CHOSE_AWARD = auto()
    HELP_CHOSE_DESCRIPTION = auto()
    HELP_CHECKING_REQUEST = auto()
    HELP_SUBJECT_AGAIN = auto()
    HELP_SUBJECT_OTHER_AGAIN = auto()
    HELP_TYPE_AGAIN = auto()
    HELP_AWARD_AGAIN = auto()
    HELP_DESCRIPTION_AGAIN = auto()
    HELP_MATCHING = auto()
    HELP_MATCHED = auto()
