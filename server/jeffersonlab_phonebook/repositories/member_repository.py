from datetime import date
from typing import Any, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from jeffersonlab_phonebook.db.models import Member
from jeffersonlab_phonebook.schemas.members_schemas import MemberCreate, MemberUpdate # Import the schemas

class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sub(self, sub: str) -> Member | None:
        """
        Retrieves a member by their 'sub' identifier stored in experimental_data.
        """
        return self.db.scalar(
            select(Member).where(Member.experimental_data["sub"].astext == sub)
        )

    def get(self, member_id: int) -> Member | None:
        """
        Retrieves a single member by their primary key ID.
        Eagerly loads the 'institution' relationship for nested serialization.
        """
        return self.db.scalar(
            select(Member)
            .options(joinedload(Member.institution))
            .where(Member.id == member_id)
        )

    def create(self, member_in: MemberCreate) -> Member:
        """
        Creates a new member in the database from a MemberCreate Pydantic model.
        This method is designed to be called directly by the FastAPI router.
        If creating from OAuth userinfo, map userinfo to MemberCreate first.
        """
        # Convert MemberCreate Pydantic model to a dictionary
        # and create a Member ORM object.
        # This will include all fields from MemberCreate, handling Optional values correctly.
        member_data = member_in.model_dump(exclude_unset=False) # include unset to ensure all fields from schema are considered
        
        # Ensure experimental_data is a dictionary if it's coming from an OAuth flow
        # If your MemberCreate schema handles experimental_data as Optional[dict],
        # then this might be optional based on your flow.
        if 'experimental_data' in member_data and member_data['experimental_data'] is None:
             member_data['experimental_data'] = {} # Ensure it's an empty dict if None
        
        member = Member(**member_data)
        
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    # --- Adaptation for OAuth callback's create method ---
    # You might want to keep a separate method for the OAuth flow
    # or adapt `create` to handle both. For clarity, keeping the original
    # `create_from_oauth_userinfo` and having `create` use MemberCreate.
    def create_from_oauth_userinfo(self, userinfo: dict, institution_id: int) -> Member:
        """
        Specific method to create a member during the OAuth callback.
        This adapts the userinfo dict to the MemberCreate schema before calling the generic create.
        """
        try:
            given_name = userinfo["given_name"]
            family_name = userinfo["family_name"]
            email = userinfo["email"]
        except KeyError as e:
            raise ValueError(f"Missing required userinfo field for OAuth member creation: {e}") from e

        # Construct MemberCreate from userinfo
        member_create_data = MemberCreate(
            first_name=given_name,
            last_name=family_name,
            email=email,
            orcid=userinfo.get("eduPersonOrcid"),
            institution_id=institution_id,
            date_joined=date.today(),
            is_active=True, # Default for new OAuth users
            experimental_data={
                "sub": userinfo.get("sub")
            },
        )
        return self.create(member_create_data) # Use the generic create method


    def get_all(self, skip: int = 0, limit: int = 100) -> list[Member]:
        """
        Retrieves all members from the database.
        Includes eager loading of the 'institution' relationship for nested serialization.
        """
        return list(
            self.db.scalars(
                select(Member).offset(skip).limit(limit).options(joinedload(Member.institution))
            ).all()
        )
    
    def count_all(self) -> int:
        """
        Returns the total number of members in the database.
        """
        count = self.db.scalar(select(func.count()).select_from(Member))
        return count or 0

    def update(self, db_member: Member, member_in: MemberUpdate) -> Member:
        """
        Updates an existing member in the database.
        Only fields provided in member_in (i.e., not None or unset) will be updated.
        """
        # model_dump(exclude_unset=True) gets only the fields that were
        # explicitly set by the client in the request body, ignoring default
        # values of Optional fields.
        update_data = member_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "experimental_data":
                # If experimental_data is provided, replace the whole dict
                # If you need to merge or partially update experimental_data,
                # you'd need more specific logic here (e.g., recursive update).
                setattr(db_member, key, value if value is not None else {}) # ensure it's a dict or empty dict
            else:
                setattr(db_member, key, value)

        self.db.add(db_member) # Add back to session to track changes
        self.db.commit()
        self.db.refresh(db_member)
        return db_member

    def delete(self, member_id: int) -> None:
        """
        Deletes a member from the database by ID.
        Raises an error if the member does not exist (though the router typically handles this check).
        """
        member = self.db.scalar(select(Member).where(Member.id == member_id))
        if member:
            self.db.delete(member)
            self.db.commit()
        # If member is None, the router's get/delete logic should already raise 404
        # or handle it before calling this. This method assumes the member exists
        # or silently does nothing if not found, but it's safer to rely on the
        # router's check for 404.
    
    def get_member_by_institution(
        self, institution_id: int, skip: int = 0, limit: int = 100
    ) -> list[Member]:
        """
        Retrieves members for a specific institution, with optional pagination.
        """
        return list(
            self.db.scalars(
                select(Member)
                .options(joinedload(Member.institution))  # eager-load institution
                .where(Member.institution_id == institution_id)
                .offset(skip)
                .limit(limit)
            ).all()
        )

