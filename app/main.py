from typing import List
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.Models.User import User
from .Database.databaseConexion import sessionLocal
from .Schemas.user import UserBase
from .Schemas.response import Response
from .JWT.JWTManager import create_token, validate_token

from app.JWT import encrypt


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return "Hello World!"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        user_db = db.query(User).filter(User.user == data['user']).first()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Credenciales incorrectas"
            )
        return auth


def authenticate_user(db, username: str, password: str):
    user_db = db.query(User).filter(User.user == username).first()
    if user_db and encrypt.verify_password(password, user_db.password):
        return user_db


@app.get('/users', response_model=List[UserBase], dependencies=[Depends(JWTBearer())])
def get_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/add_user", response_model=UserBase)
def create_user(schema: UserBase, db: Session = Depends(get_db)):
    hashed_password = encrypt.hash_password(schema.password)
    user_for_insert = User(user=schema.user, password=hashed_password)
    db.add(user_for_insert)
    db.commit()
    db.refresh(user_for_insert)
    return user_for_insert


@app.delete("/delete_user/{user_id}", response_model=Response)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con id {user_id} no encontrado")

    db.delete(user)
    db.commit()
    response = Response(message=f"Usuario con id {user_id} fue eliminado correctamente")
    return response


@app.post("/login", tags=['auth'])
def login_for_access_token(db: Session = Depends(get_db), user_data: UserBase = Depends()):
    user = authenticate_user(db, user_data.user, user_data.password)
    if user:
        token_data: str = create_token(user_data.model_dump())
        return JSONResponse(status_code=200, content=token_data)



