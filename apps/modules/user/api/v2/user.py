from fastapi import APIRouter
from apps.ext.jwtAuth import auth_handler
from apps.modules.user.schemas.user import AuthDetails
# from apps.ext.sqlalchemy.model import User

from fastapi_extend import pagenator, serializer
from apps.response.json_response import resp, resp_error
from fastapi import Depends

router = APIRouter()


@router.post('/login')
async def login(auth_details: AuthDetails):
    payload = {
        "userName": auth_details.username.lower()
    }
    token = auth_handler.encode_token(payload)
    return resp(data={"Authorization": token})


@router.get('/getUser')
async def get_user(_user=Depends(auth_handler.auth_wrapper)):
    pass
