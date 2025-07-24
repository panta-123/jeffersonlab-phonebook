from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# We need to import the GroupRole enum
from jeffersonlab_phonebook.db.constants import GroupRole

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
    
    # You might want to include the list of members in the response
    # For that, you would need to define and import MemberResponse
    # and create a GroupWithMembersResponse schema
    
    model_config = ConfigDict(from_attributes=True)

# Schema for the associative table
class GroupMemberBase(BaseModel):
    group_id: int
    member_id: int
    role: GroupRole

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberResponse(GroupMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)