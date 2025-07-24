import enum

class BoardType(enum.Enum):
    INSTITUTIONAL = "institutional"
    EXECUTIVE = "executive"

class GroupRole(enum.Enum):
    MEMBER = "member"
    CONVENOR = "convenor"
    CO_CONVENOR = "co-convenor"