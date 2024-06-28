from database import db
from sqlalchemy import Column, Integer, String


class UserModel(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String, nullable=False)
