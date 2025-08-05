from datetime import date
from typing import Any

from sqlalchemy import Date, Float, ForeignKey, String, Enum, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .constants import BoardType


class Base(DeclarativeBase):
    pass


class Role(Base):
    """
    Represents a dynamic role that can be assigned to members in various contexts.
    This allows administrators to add new roles without code changes.
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships to models that use this role
    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="role"
    )
    board_memberships: Mapped[list["InstitutionalBoardMember"]] = relationship(
        back_populates="role"
    )
    # New: Relationship for roles in talk assignments
    talk_assignments: Mapped[list["TalkAssignment"]] = relationship(
        back_populates="role"
    )


class Institution(Base):
    """Represents an academic or research institution."""

    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    entityid: Mapped[str] = mapped_column(String)
    rorid: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String(50))
    short_name: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)

    date_added: Mapped[date] = mapped_column(Date, nullable=False)
    date_removed: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    experimental_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )

    members: Mapped[list["Member"]] = relationship(back_populates="institution")
    institution_memberships: Mapped[list["MemberInstitutionHistory"]] = relationship(
        back_populates="institution"
    )
    board_memberships: Mapped[list["InstitutionalBoardMember"]] = relationship(
        back_populates="institution"
    )


class Member(Base):
    """Represents a person in the collaboration."""

    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    orcid: Mapped[str | None] = mapped_column(String, nullable=True)
    preferred_author_name: Mapped[str | None] = mapped_column(String, nullable=True)

    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    date_joined: Mapped[date] = mapped_column(Date, nullable=False)
    date_left: Mapped[date | None] = mapped_column(Date, nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)

    experimental_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )

    institution: Mapped["Institution"] = relationship(back_populates="members")
    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="member"
    )
    institution_history: Mapped[list["MemberInstitutionHistory"]] = relationship(
        back_populates="member"
    )
    board_memberships: Mapped[list["InstitutionalBoardMember"]] = relationship(
        back_populates="member"
    )
    # New: Relationships for talks and assignments
    talk_assignments: Mapped[list["TalkAssignment"]] = relationship(
        back_populates="member", foreign_keys="TalkAssignment.member_id"
    )
    talk_assignments_given: Mapped[list["TalkAssignment"]] = relationship(
        back_populates="assigned_by_member", foreign_keys="TalkAssignment.assigned_by_id"
    )


class MemberInstitutionHistory(Base):
    """Tracks the history of a member's association with institutions."""

    __tablename__ = "member_institution_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    member: Mapped["Member"] = relationship(back_populates="institution_history")
    institution: Mapped["Institution"] = relationship(
        back_populates="institution_memberships"
    )


class Group(Base):
    """Represents a working group with a hierarchical structure."""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_created: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Hierarchical relationship
    parent_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id"), nullable=True
    )
    parent_group: Mapped["Group"] = relationship(
        "Group", remote_side=[id], back_populates="subgroups"
    )
    subgroups: Mapped[list["Group"]] = relationship(
        "Group", back_populates="parent_group", cascade="all, delete-orphan"
    )

    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="group"
    )


class GroupMember(Base):
    """Associative table linking members to groups."""

    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False, default=1
    )  # Assuming role with ID 1 is the default
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    group: Mapped["Group"] = relationship(back_populates="group_memberships")
    member: Mapped["Member"] = relationship(back_populates="group_memberships")
    role: Mapped["Role"] = relationship(back_populates="group_memberships")


class InstitutionalBoardMember(Base):
    """
    Associative table linking members to institutional boards with specific roles and tenure.
    """

    __tablename__ = "institutional_board_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))

    board_type: Mapped[BoardType] = mapped_column(Enum(BoardType), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    member: Mapped["Member"] = relationship(back_populates="board_memberships")
    institution: Mapped["Institution"] = relationship(
        back_populates="board_memberships"
    )
    role: Mapped["Role"] = relationship(back_populates="board_memberships")



class Conference(Base):
    """Represents a conference or meeting where talks are given."""

    __tablename__ = "conferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    url: Mapped[str | None] = mapped_column(String, nullable=True)

    talks: Mapped[list["Talk"]] = relationship(back_populates="conference")


class Talk(Base):
    """Represents a specific presentation assigned to a member."""

    __tablename__ = "talks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    docdb_id: Mapped[str | None] = mapped_column(String, nullable=True)
    talk_link: Mapped[str | None] = mapped_column(String, nullable=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    conference_id: Mapped[int | None] = mapped_column(ForeignKey("conferences.id"))
    conference: Mapped["Conference"] = relationship(back_populates="talks")

    assignments: Mapped[list["TalkAssignment"]] = relationship(
        back_populates="talk"
    )


class TalkAssignment(Base):
    """
    Associative table linking a member to a talk with a specific role.
    This is where talks are assigned by the committee.
    """

    __tablename__ = "talk_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    talk_id: Mapped[int] = mapped_column(ForeignKey("talks.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    assigned_by_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"))
    assignment_date: Mapped[date] = mapped_column(Date, nullable=False)

    talk: Mapped["Talk"] = relationship(back_populates="assignments")
    member: Mapped["Member"] = relationship(
        back_populates="talk_assignments", foreign_keys=[member_id]
    )
    role: Mapped["Role"] = relationship(back_populates="talk_assignments")
    assigned_by_member: Mapped["Member"] = relationship(
        back_populates="talk_assignments_given", foreign_keys=[assigned_by_id]
    )
