from app.Database.databaseConexion import base
from sqlalchemy import Column, Integer, String


class User(base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String(100))
    password = Column(String(100))



