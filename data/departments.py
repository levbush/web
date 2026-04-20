import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


C = sqlalchemy.Column
Int = sqlalchemy.Integer
Str = sqlalchemy.String


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = C(Int, primary_key=True, autoincrement=True)
    title = C(Str, nullable=True)
    chief = C(Int, sqlalchemy.ForeignKey('users.id'))
    members = C(Str, nullable=True)
    email = C(Str, index=True, unique=True, nullable=True)

    user = orm.relationship('User')

    def __repr__(self):
        return f'<Department> {self.id} {self.title} {self.email}'