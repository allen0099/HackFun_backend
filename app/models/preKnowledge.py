from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app import db


class Knowledge(db.Model):
    __tablename__: str = "knowledge"

    id: Column = db.Column(
        db.Integer,
        primary_key=True
    )
    text: Column = db.Column(
        db.String(1000),
        unique=True,
        nullable=False
    )

    lesson: relationship = db.relationship(
        "Lesson",
        backref="knowledge",
        lazy="dynamic"
    )

    def __repr__(self) -> str:
        return "<Tab %r>" % self.tab
