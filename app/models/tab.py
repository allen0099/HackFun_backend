from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app import db


class Tab(db.Model):
    __tablename__: str = "tab"

    id: Column = db.Column(db.Integer,
                           primary_key=True)

    name: Column = db.Column(db.String(15),
                             unique=True,
                             nullable=False)

    course: relationship = db.relationship("Course",
                                           backref="tab",
                                           lazy="dynamic")

    def __repr__(self) -> str:
        return "<Tab %r>" % self.tab
