import enum

class BoardType(enum.Enum):
    INSTITUTIONAL = "institutional"
    EXECUTIVE = "executive"
    PUBLICATION = "publication"
    TALKS = "talks"

class GroupRole(enum.Enum):
    MEMBER = "members"
    CONVENOR = "convenor"
    CO_CONVENOR = "co-convenor"