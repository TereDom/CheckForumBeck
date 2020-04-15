import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class WikiDB(SqlAlchemyBase, UserMixin):
    __tablename__ = 'wiki_base'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
