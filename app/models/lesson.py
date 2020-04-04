from sqlalchemy.orm import relationship

from app import db
from app.models import uuid


class Lesson(db.Model):
    __tablename__ = "lesson"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    uuid: str = db.Column(
        db.String(64),
        default=uuid.generate("lesson-"),
        unique=True,
        nullable=False
    )
    belong: str = db.Column(
        db.String(50),
        db.ForeignKey("course.name")
    )
    lid: int = db.Column(
        db.Integer
    )
    name: str = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    desc: str = db.Column(
        db.Text
    )
    url: str = db.Column(
        db.Text
    )

    practices: relationship = db.relationship(
        "Practice",
        backref="lesson",
        lazy="dynamic"
    )

    def __init__(
            self,
            belong: str,
            name: str,
            desc: str = None,
            url: str = None
    ) -> None:
        self.belong = belong
        self.name = name
        self.desc = desc
        self.url = url

    def __repr__(self) -> str:
        return "<Lesson %s>" % self.name
