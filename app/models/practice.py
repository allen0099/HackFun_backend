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
        default=uuid.generate(),
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

    choose: relationship = db.relationship(
        "Choose",
        backref="practice",
        lazy="dynamic"
    )
    docker: relationship = db.relationship(
        "Docker",
        backref="practice",
        lazy="dynamic"
    )
    hint: relationship = db.relationship(
        "Hint",
        backref="practice",
        lazy="dynamic"
    )

    def __init__(
            self,
            belong: int,
            name: str
    ) -> None:
        self.belong = belong
        self.name = name  # 大標題

    def __repr__(self) -> str:
        return f"<Practice {self.name}>"
