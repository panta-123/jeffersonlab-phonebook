from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.institution_repository import (
    InstitutionRepository,
)
from jeffersonlab_phonebook.repositories.member_repository import MemberRepository

from ...config.settings import settings
from ..deps import get_db

router = APIRouter(prefix="/user", tags=["user"])

# 1. Initialize Authlib OAuth client
oauth = OAuth()
oauth.register(
    name="cilogon",
    client_id=settings.CILOGON_CLIENT_ID,
    client_secret=settings.CILOGON_CLIENT_SECRET,
    server_metadata_url=settings.CILOGON_DISCOVERY_URL,
    client_kwargs={"scope": "openid email profile org.cilogon.userinfo"},
)


# 2. Create the login route to redirect the user to CILogon
@router.get("/login")
async def login(request: Request):
    """_summary_

    :param Request request: _description_
    :return _type_: _description_
    """
    redirect_uri = request.url_for("callback")
    return await oauth.cilogon.authorize_redirect(request, redirect_uri)


# 3. Create the callback route to handle the return from CILogon
@router.get("/callback")
async def auth(request: Request, db: Session = Depends(get_db)):
    """_summary_

    :param Request request: _description_
    :param Session db: _description_, defaults to Depends(get_db)
    :return _type_: _description_
    """
    token = await oauth.cilogon.authorize_access_token(request)
    userinfo = token.get("userinfo")

    if not userinfo:
        return {"error": "Could not fetch user info"}

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

    # Here you would typically create a session for the user (e.g., a JWT)
    # and return it. For simplicity, we return the member info.
    # Note: You'll need to add session management middleware to your main app.
    request.session["user"] = userinfo

    # Redirect user to the frontend or a logged-in page
    return RedirectResponse(url="/")  # Or some other destination
