from passlib.hash import bcrypt
from datetime import datetime, timedelta
import tables
from models.auth import User, Token, UserCreate
from jose import JWSError, jwt
from settings import settings
from fastapi import status, HTTPException, Depends
import tables
from database import get_session
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Для связи с фастапи"""
    return AuthService.verify_token(token)

class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> User:
        """проверка токена"""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithms]
            )
        except JWSError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # Достаем пользователя
        user_data = payload.get("user")
        try:
            user = User.parse_obj(user_data)
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.utcnow()

        payload = {
            "iat": now, # время выпуска токена
            "nbf": now, # время начала действия
            "exp": now + timedelta(settings.jwt_expiration),# время жизни токена
            "sub": str(user_data.id),
            "user": user_data.dict()
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithms
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        """сразу регистрация и авторизация"""
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password)

        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, user_name: str, password: str) -> Token:
        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.username == user_name)
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not self.verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return self.create_token(user)

