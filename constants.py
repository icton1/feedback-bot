from enum import Enum, auto
import enum


class State(Enum):
    FIRST_NODE = auto()
    REVIEW = auto()

    HELP_INLINE_CHOOSING = auto()


class CallbackQueryAnswer(enum.IntEnum):
    HELP_POP_SUBJ1 = auto()
    HELP_POP_SUBJ2 = auto()
    HELP_POP_SUBJ3 = auto()
    HELP_POP_SUBJ_OTHER = auto()
