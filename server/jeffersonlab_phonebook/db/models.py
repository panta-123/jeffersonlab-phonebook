from datetime import date
from typing import Any

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Institution(DeclarativeBase):
    """Represents an academic or research institution."""

    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
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


class Member(DeclarativeBase):
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


class MemberInstitutionHistory(DeclarativeBase):
    """Tracks the history of a member's association with institutions."""

    __tablename__ = "member_institution_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    member = relationship("Member")
    institution = relationship("Institution")


class Group(DeclarativeBase):
    """Represents a working group that includes members."""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="group"
    )


class GroupMember(DeclarativeBase):
    """Associative table linking members to groups."""

    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    group: Mapped["Group"] = relationship(back_populates="group_memberships")
    member: Mapped["Member"] = relationship(back_populates="group_memberships")


class Event(DeclarativeBase):
    """Represents an event with a name, date, and optional location."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(Date)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
