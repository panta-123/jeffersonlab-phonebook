from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# We need to import the GroupRole enum
from jeffersonlab_phonebook.db.constants import GroupRole

# --- Group Schemas ---
# Base Schema
class GroupBase(BaseModel):
    name: str

# Create Schema
class GroupCreate(GroupBase):
    pass

# Update Schema
class GroupUpdate(GroupBase):
    name: Optional[str] = None

# Response Schema
class GroupResponse(GroupBase):
    id: int

    # You might want to include the list of members in the response later.
    # For example, if you have a MemberResponse schema:
    # members: List["MemberResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# --- GroupMember Schemas ---
# Base Schema for the associative table
class GroupMemberBase(BaseModel):
    group_id: int
    member_id: int
    role: GroupRole

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberUpdate(BaseModel): # Added this schema for updating GroupMember
    role: Optional[GroupRole] = None

class GroupMemberResponse(GroupMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)