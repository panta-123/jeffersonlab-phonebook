from datetime import date
from typing import Any

from sqlalchemy import Date, Float, ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .constants import BoardType, GroupRole


class Base(DeclarativeBase):
    pass

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


class MemberInstitutionHistory(Base):
    """Tracks the history of a member's association with institutions."""

    __tablename__ = "member_institution_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    member = relationship("Member")
    institution = relationship("Institution")


class Group(Base):
    """Represents a working group that includes members."""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="group"
    )


class GroupMember(Base):
    """Associative table linking members to groups."""

    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    role: Mapped[GroupRole] = mapped_column(
        Enum(GroupRole), nullable=False, default=GroupRole.MEMBER
    )

    group: Mapped["Group"] = relationship(back_populates="group_memberships")
    member: Mapped["Member"] = relationship(back_populates="group_memberships")


class InstitutionalBoardMember(Base):
    """
    Associative table linking members to institutional boards with specific roles and tenure.
    """
    __tablename__ = "institutional_board_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))

    board_type: Mapped[BoardType] = mapped_column(
        Enum(BoardType), nullable=False
    )
    role: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    member: Mapped["Member"] = relationship(back_populates="board_memberships")
    institution: Mapped["Institution"] = relationship(back_populates="board_memberships")

    # This could be useful if you need a chair for the board itself
    is_chair: Mapped[bool] = mapped_column(default=False)

