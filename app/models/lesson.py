from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app import db
from app.models.uuid import generate


class Lesson(db.Model):
    __tablename__: str = "lesson"

    id: Column = db.Column(
        db.Integer,
        primary_key=True
    )
    uuid: Column = db.Column(
        db.String(64),
        default=generate("lesson-"),
        unique=True,
        nullable=False
    )
    belong: Column = db.Column(
        db.String(50),
        db.ForeignKey("course.name")
    )
    name: Column = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    description: Column = db.Column(
        db.Text
    )
    url: Column = db.Column(
        db.Text
    )

    practices: relationship = db.relationship(
        "Practice",
        backref="lesson",
        lazy="dynamic"
    )

    def __repr__(self) -> str:
        return "<Lesson %r>" % self.name
