from fastapi import APIRouter
from sqlalchemy import select
from apps.ext.jwtAuth import auth_handler
from apps.modules.user.schemas.user import AuthDetails
from apps.ext.sqlalchemy.model import User
from fastapi_extend import PageNumberPagination
from apps.ext.sqlalchemy import db_connect
from apps.modules.user.schemas.user import GetUser, UserSer
from apps.response.json_response import resp
from fastapi import Depends

router = APIRouter()


@router.post('/login')
async def login(auth_details: AuthDetails):
    payload = {
        "userName": auth_details.username.lower()
    }
    token = auth_handler.encode_token(payload)
    return resp(data={"Authorization": token})


@router.post('/getUser')
async def get_user(
              params: GetUser,
              _user=Depends(auth_handler.auth_wrapper)):
    async with db_connect.async_session() as session:
        paginator = PageNumberPagination(
            params,
            User,
            UserSer,
            exclude={"col_id"},
        )
        query = paginator.get_queryset()
        if params.col_id:
            query = query.where(User.id == params.col_id)
        data = await paginator.paginate_query(query, session)
        return data
        # data = await session.execute(select(User))
        # data = data.scalars()
        # if data:
        #     results = [each.to_dict() for each in data]
        #     return resp(results)



