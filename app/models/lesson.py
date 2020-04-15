from sqlalchemy.orm import relationship

from app import db
from app.models import uuid


class Lesson(db.Model):
    __tablename__: str = "lesson"

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
    belong: str = db.Column(
        db.String(50),
        db.ForeignKey("course.name")
    )
    order_id: int = db.Column(
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
    vid_url: str = db.Column(
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
            order_id: int,
            name: str,
            desc: str = None,
            vid_url: str = None
    ) -> None:
        self.belong = belong
        self.order_id = order_id
        self.name = name
        self.desc = desc
        self.vid_url = vid_url

    def __repr__(self) -> str:
        return f"<Lesson {self.name}>"
