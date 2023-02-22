import datetime
from datetime import timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.db.db import get_session
from src.core.settings import settings
from src.models.schemas.utils.jwt_token import JwtToken
from src.models.user import User
from src.models.schemas.user.user_request import UserRequest

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/users/authorize')


def get_current_user_id(token: str = Depends(oauth2_schema)):
    return UsersService.verify_token(token)


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    def create_token(user_id: int) -> JwtToken:
        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id)
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.encode(token, settings.jwt_secret, algorithm=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')

        return payload.get('sub')

    def register(self, user_schema: UserRequest) -> None:
        user = User(
            username=user_schema.username,
            password_hash=self.hash_password(user_schema.password_text)
        )
        self.session.add(user)
        self.session.commit()

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (self.session
                .query(User)
                .filter(User.username == username)
                .first()
                )

        if not user:
            return None
        if not self.check_password(password_text, user.password_hash):
            return None

        return self.create_token(user.id)

