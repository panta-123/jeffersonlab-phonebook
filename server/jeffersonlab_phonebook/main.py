from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from jeffersonlab_phonebook.api.main import api_router
from jeffersonlab_phonebook.config.settings import settings
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

class ForceHTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        response = await call_next(request)
        return response

def custom_generate_unique_id(route: APIRoute) -> str:
    """_summary_

    :param APIRoute route: _description_
    :return str: _description_
    """
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(ForceHTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["vulcan.jlab.org"])

app.include_router(api_router, prefix=settings.API_V1_STR)
