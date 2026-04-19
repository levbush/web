import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


C = sqlalchemy.Column
Int = sqlalchemy.Integer
Str = sqlalchemy.String


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = C(Int, primary_key=True, autoincrement=True)
    job = C(Str, nullable=True)
    work_size = C(Int, nullable=True, default=0)
    collaborators = C(Str, nullable=True)
    team_leader = C(Int, sqlalchemy.ForeignKey("users.id"))
    start_date = C(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = C(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_finished = C(sqlalchemy.Boolean, default=False)

    user = orm.relationship('User', foreign_keys=[team_leader])