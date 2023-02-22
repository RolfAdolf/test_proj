from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.models.schemas.user.user_request import UserRequest
from src.services.users import UsersService
from src.models.schemas.utils.jwt_token import JwtToken

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация')
def register(user_schema: UserRequest, users_service: UsersService = Depends()):
    return users_service.register(user_schema)


@router.post('/authorize', response_model=JwtToken, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()):
    result = users_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return result
