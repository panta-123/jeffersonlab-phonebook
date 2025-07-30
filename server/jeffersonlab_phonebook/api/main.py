from fastapi import APIRouter

from jeffersonlab_phonebook.api.routes import institutions, login, members, board_members, groups, utils

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(institutions.router)
api_router.include_router(members.router)
api_router.include_router(utils.router)
api_router.include_router(board_members.router)
api_router.include_router(groups.router)
