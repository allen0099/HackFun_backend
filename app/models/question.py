from sqlalchemy.orm import relationship

from app import db


class Question(db.Model):
    __tablename__: str = "question"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: int = db.Column(
        db.Integer,
        db.ForeignKey("practice.id")
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )

    options: relationship = db.relationship(
        "Options",
        backref="question",
        lazy="dynamic"
    )

    def __init__(self, belong, desc) -> None:
        self.belong = belong
        self.desc = desc  # 題目描述

    def __repr__(self) -> str:
        return f"<Question {self.id}>"
