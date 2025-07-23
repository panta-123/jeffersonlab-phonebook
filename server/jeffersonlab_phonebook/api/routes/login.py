"""_summary_"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.institution_repository import (
    InstitutionRepository,
)
from jeffersonlab_phonebook.repositories.member_repository import MemberRepository

from ..deps import create_jwt_and_cookie, get_db, get_oauth

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/login")
async def login(request: Request, oauth=Depends(get_oauth)):
    """_summary_

    :param Request request: _description_
    :return _type_: _description_
    """
    redirect_uri = request.url_for("callback")
    return await oauth.cilogon.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth(
    request: Request, db: Session = Depends(get_db), oauth=Depends(get_oauth)
):
    """_summary_

    :param Request request: _description_
    :param Session db: _description_, defaults to Depends(get_db)
    :return _type_: _description_
    """
    try:
        token = await oauth.cilogon.authorize_access_token(request)
        userinfo = token.get("userinfo")
    except Exception as e:
        # Log this error for debugging in production
        print(f"OAuth authorization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth authorization failed or user denied access.",
        ) from e

    if not userinfo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not fetch user info from OAuth provider.",
        )

    member_repo = MemberRepository(db)
    institution_repo = InstitutionRepository(db)

    member = member_repo.get_by_sub(userinfo["sub"])

    if not member:
        institution = institution_repo.get_by_name(
            userinfo.get("idp_name", "Default Institution")
        )
        if not institution:
            institution = institution_repo.create(
                userinfo.get("idp_name", "Default Institution"), userinfo
            )

        member = member_repo.create(userinfo, institution.id)
    elif not member.is_active:
        # If the member is inactive, you might want to handle this case
        return {"error": "Member is inactive"}

    return create_jwt_and_cookie(member, userinfo)


@router.post("/logout")
async def logout(response: Response):
    """Clears the access_token cookie to log the user out."""
    response.delete_cookie(
        key="access_token", httponly=True, secure=True, samesite="lax", path="/"
    )
    return {"message": "Logged out successfully"}
