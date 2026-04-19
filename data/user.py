import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


C = sqlalchemy.Column
Int = sqlalchemy.Integer
Str = sqlalchemy.String


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = C(Int, primary_key=True, autoincrement=True)
    surname = C(Str, nullable=True)
    name = C(Str, nullable=True)

    age = C(Int, nullable=True)
    position = C(Str, nullable=True)
    speciality = C(Str, nullable=True)
    address = C(Str, nullable=True)

    email = C(Str, nullable=True, unique=True)

    hashed_password = C(Str, nullable=True)
    modified_date = C(sqlalchemy.DateTime, default=datetime.datetime.now)


