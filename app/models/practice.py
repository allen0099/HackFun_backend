from sqlalchemy.orm import relationship

from app import db
from app.models import uuid


class Practice(db.Model):
    __tablename__ = "practice"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    uuid: str = db.Column(
        db.String(64),
        default=uuid.generate(""),
        unique=True,
        nullable=False
    )
    belong: int = db.Column(
        db.Integer,
        db.ForeignKey("lesson.id")
    )
    name: str = db.Column(
        db.String(25),
        nullable=False
    )
    type: str = db.Column(
        db.String(20),
        nullable=False
    )

    hint: relationship = db.relationship(
        "Hint",
        backref="practice",
        lazy="dynamic"
    )
    question: relationship = db.relationship(
        "Question",
        backref="practice",
        lazy="dynamic"
    )
    docker: relationship = db.relationship(
        "Docker",
        backref="practice",
        lazy="dynamic"
    )

    def __init__(
            self,
            belong: int,
            name: str,
            type: str
    ) -> None:
        self.belong = belong
        self.name = name  # 大標題
        self.type = type  # 種類, docker 或是 choose

    def __repr__(self) -> str:
        return "<Practice %r>" % self.name
