"""_summary_"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from jeffersonlab_phonebook.config.settings import settings
from datetime import date


from jeffersonlab_phonebook.repositories.institution_repository import (
    InstitutionRepository,
)
from jeffersonlab_phonebook.repositories.member_repository import MemberRepository
from jeffersonlab_phonebook.schemas.institutions_schemas import InstitutionCreate
from jeffersonlab_phonebook.schemas.auth_schemas import AuthStatus, ErrorDetail
from jeffersonlab_phonebook.db.session import get_db
from ..deps import create_jwt_and_cookie, get_oauth

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/login")
async def login(request: Request, oauth=Depends(get_oauth)):
    """_summary_

    :param Request request: _description_
    :return _type_: _description_
    """
    redirect_uri = request.url_for("login:callback")
    return await oauth.cilogon.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="login:callback")
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
        print(f"Received token: {token}") 
        # -----------------------------------        
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
            # Create the Pydantic model instance first
            institution_data = InstitutionCreate(
                full_name=userinfo.get("idp_name", "Default Institution"),
                short_name=userinfo.get("idp_name", "Default Institution"),
                date_added=date.today(),
                country=userinfo.get("country", "US"),
            )
            institution = institution_repo.create(institution_data)

        member = member_repo.create_from_oauth_userinfo(userinfo, institution.id)
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


@router.get(
    "/check-auth",
    response_model=AuthStatus,
    responses={
        401: {"model": ErrorDetail, "description": "Unauthorized: Token expired or invalid"},
        500: {"model": ErrorDetail, "description": "Internal Server Error"}
    }
)
async def check_auth_status(request: Request, db: Session = Depends(get_db)):
    """
    Checks the authentication status of the user based on the access_token cookie
    and returns their authentication status, admin status, email, and name.
    """
    access_token_cookie = request.cookies.get("access_token")

    if not access_token_cookie:
        # No token, user is not authenticated. Return all fields as None/False.
        return AuthStatus(authenticated=False, isAdmin=False, email=None, name=None)

    try:
        # Decode the JWT token
        payload = jwt.decode(
            access_token_cookie,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True} # pyjwt can automatically verify expiration
        )

        # Extract 'is_admin', 'email', and 'name' from the payload
        is_admin = payload.get("isadmin", False) # Default to False if not present
        user_email = payload.get("email") # Get email from payload
        user_name = payload.get("name")   # Get name from payload

        return AuthStatus(
            authenticated=True,
            isAdmin=is_admin,
            email=user_email, # Include extracted email
            name=user_name    # Include extracted name
        )

    except ExpiredSignatureError:
        print("ExpiredSignatureError: Token has expired.")
        # Raise 401 Unauthorized for expired tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired.",
            headers={"WWW-Authenticate": "Bearer error=\"token_expired\""}
        )
    except InvalidTokenError:
        print("InvalidTokenError: Invalid token detected during check-auth.")
        # Raise 401 Unauthorized for invalid tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer error=\"invalid_token\""}
        )
    except Exception as e:
        print(f"An unexpected error occurred during check-auth: {e}")
        # Raise 500 Internal Server Error for unhandled exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred during authentication check."
        )
