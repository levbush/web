import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


C = sqlalchemy.Column
Int = sqlalchemy.Integer
Str = sqlalchemy.String

jobs_to_categories = sqlalchemy.Table(
    'jobs_to_categories',
    SqlAlchemyBase.metadata,
    C('job_id', Int, sqlalchemy.ForeignKey('jobs.id')),
    C('category_id', Int, sqlalchemy.ForeignKey('categories.id')),
)


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = C(Int, primary_key=True, autoincrement=True)
    name = C(Str, nullable=True)

    def __repr__(self):
        return f'<Category> {self.id} {self.name}'