from fastapi import APIRouter

from jeffersonlab_phonebook.api.routes import institutions, login, members, board_members, groups, utils, role, talk_conference, talk_assignment

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(institutions.router)
api_router.include_router(members.router)
api_router.include_router(utils.router)
api_router.include_router(board_members.router)
api_router.include_router(groups.router)
api_router.include_router(role.router)
api_router.include_router(talk_conference.conference_router)
api_router.include_router(talk_conference.router)
api_router.include_router(talk_assignment.router)
