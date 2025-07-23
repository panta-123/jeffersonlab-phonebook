from datetime import datetime, timedelta, timezone

import jwt
from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse

from jeffersonlab_phonebook.config.settings import settings
from jeffersonlab_phonebook.db.session import get_db as get_db_session


def get_db():
    """_summary_

    :return _type_: _description_
    """
    return get_db_session


def get_oauth() -> OAuth:
    """_summary_

    :return OAuth: _description_
    """
    oauth = OAuth()
    oauth.register(
        name="cilogon",
        client_id=settings.CILOGON_CLIENT_ID,
        client_secret=settings.CILOGON_CLIENT_SECRET,
        server_metadata_url=settings.CILOGON_DISCOVERY_URL,
        client_kwargs={"scope": "openid email profile org.cilogon.userinfo"},
    )
    return oauth


JWT_SECRET = "your-secret-key"  # Use a secure secret in production
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600


def create_jwt_and_cookie(member, userinfo, redirect_url="/"):
    """_summary_

    :param _type_ member: _description_
    :param _type_ userinfo: _description_
    :param str redirect_url: _description_, defaults to "/"
    :return _type_: _description_
    """
    jwt_payload = {
        "sub": userinfo["sub"],
        "email": member.email,
        "name": f"{member.first_name} {member.last_name}",
        "exp": datetime.now(timezone.utc)
        + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
    }
    jwt_token = jwt.encode(
        jwt_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=JWT_EXP_DELTA_SECONDS,
        path="/",
    )
    return response


def get_current_user(request: Request):
    """_summary_

    :param Request request: _description_
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    :return _type_: _description_
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload  # or fetch user from DB using payload info
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
