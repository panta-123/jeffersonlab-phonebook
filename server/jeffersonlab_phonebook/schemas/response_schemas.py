from __future__ import annotations
from typing import List, Optional

from pydantic import ConfigDict, Field, BaseModel

# --- Import all necessary base schemas ---
# These are your base schemas for creating/updating models.
# They are assumed to be in their respective schema files.
from .institutions_schemas import InstitutionBase
from .group_schemas import GroupBase, GroupMemberBase
from .board_schemas import InstitutionalBoardMemberBase
from .conference_schemas import TalkBase, ConferenceBase, TalkAssignmentBase
from .members_schemas import MemberBase
from .role_schemas import RoleResponse
from .history_schemas import MemberInstitutionHistoryBase

# --- Lite Schemas (for use in nested relationships) ---
# These schemas contain only essential fields and are used to prevent recursion
# when a relationship points back to the parent object.

class GroupLiteResponse(GroupBase):
    """A simplified schema for Group, without nested relationships."""
    id: int
    model_config = ConfigDict(from_attributes=True)

class InstitutionLiteResponse(InstitutionBase):
    """A simplified schema for Institution, without nested relationships."""
    id: int
    model_config = ConfigDict(from_attributes=True)

class MemberLiteResponse(MemberBase):
    """A simplified schema for Member, with basic institution details."""
    id: int
    # This is safe because it points to a lite institution schema
    institution: Optional["InstitutionLiteResponse"] = None
    model_config = ConfigDict(from_attributes=True)

class PaginatedMemberResponse(BaseModel):
    items: List[MemberLiteResponse]
    total: int
    skip: int
    limit: int

class ConferenceLiteResponse(ConferenceBase):
    """A simplified schema for Conference, without nested relationships."""
    id: int
    model_config = ConfigDict(from_attributes=True)

class TalkLiteResponse(TalkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Full Response Schemas ---
# These are the top-level schemas returned by your API endpoints.
# They can include nested Lite schemas or other full schemas that do not create a loop.

class GroupMemberResponse(GroupMemberBase):
    """
    Response schema for a group member entry.
    Uses lite schemas for Group and Member to break the circular reference.
    """
    id: int
    # IMPORTANT: Use Lite schemas to break the loop with GroupResponse and MemberResponse
    group: "GroupLiteResponse"
    member: "MemberLiteResponse"
    role: "RoleResponse"
    model_config = ConfigDict(from_attributes=True)

class GroupResponse(GroupBase):
    """
    Full response schema for a Group.
    Uses lite schemas for parent/subgroups to prevent recursion.
    """
    id: int
    # IMPORTANT: Use the lite schema for parent/subgroups
    parent_group: Optional["GroupLiteResponse"] = None
    subgroups: list["GroupLiteResponse"] = []
    group_memberships: list["GroupMemberResponse"] = []
    model_config = ConfigDict(from_attributes=True)

class MemberInstitutionHistoryResponse(MemberInstitutionHistoryBase):
    id: int
    # Use Lite schemas for consistency and to prevent deep nesting
    member: Optional["MemberLiteResponse"] = None
    institution: Optional["InstitutionLiteResponse"] = None
    model_config = ConfigDict(from_attributes=True)

class InstitutionalBoardMemberResponse(InstitutionalBoardMemberBase):
    id: int
    # This schema correctly uses lite versions to prevent a loop
    member: "MemberLiteResponse"
    institution: "InstitutionLiteResponse"
    role: "RoleResponse"
    model_config = ConfigDict(from_attributes=True)

class TalkAssignmentResponse(TalkAssignmentBase):
    id: int
    member: "MemberLiteResponse"
    role: "RoleResponse"
    assigned_by_member: Optional["MemberLiteResponse"] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TalkResponse(TalkBase):
    id: int
    assignments: List["TalkAssignmentResponse"] = []

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class ConferenceResponse(ConferenceBase):
    id: int
    talks: List["TalkResponse"] = []
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    
class MemberResponse(MemberBase):
    """Full response schema for a Member."""
    id: int
    # This is fine as InstitutionResponse uses MemberLiteResponse
    institution: Optional["InstitutionResponse"] = None
    group_memberships: List["GroupMemberResponse"] = []
    board_memberships: List["InstitutionalBoardMemberResponse"] = []
    talk_assignments: List["TalkAssignmentResponse"] = []
    talk_assignments_given: List["TalkAssignmentResponse"] = []
    model_config = ConfigDict(from_attributes=True)

class InstitutionResponse(InstitutionBase):
    """Full response schema for an Institution."""
    id: int
    # IMPORTANT: Use MemberLiteResponse to prevent the circular reference with MemberResponse
    members: List["MemberLiteResponse"] = []
    board_memberships: List["InstitutionalBoardMemberResponse"] = []
    institution_memberships: List["MemberInstitutionHistoryResponse"] = []
    model_config = ConfigDict(from_attributes=True)


# --- Final step: Rebuild forward references ---
# This tells Pydantic to resolve the string literals into the actual classes.
# Only call it for schemas that have a forward reference.
GroupMemberResponse.model_rebuild()
GroupResponse.model_rebuild()
MemberInstitutionHistoryResponse.model_rebuild()
InstitutionalBoardMemberResponse.model_rebuild()
TalkAssignmentResponse.model_rebuild()
TalkResponse.model_rebuild()
ConferenceResponse.model_rebuild()
MemberLiteResponse.model_rebuild() # Required because it references InstitutionLiteResponse
MemberResponse.model_rebuild()
InstitutionResponse.model_rebuild()