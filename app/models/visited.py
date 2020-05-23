from datetime import datetime

from app import db


class Visited(db.Model):
    __tablename__: str = "visited"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    user_id: str = db.Column(
        db.String(30),
        db.ForeignKey("user.id"),
        nullable=False
    )
    lesson_id: int = db.Column(
        db.Integer,
        db.ForeignKey("lesson.id"),
        nullable=False
    )
    timestamp: datetime = db.Column(
        db.TIMESTAMP(),
        server_default=db.func.now()
    )

    def __init__(self,
                 user_id: str,
                 lesson_id: int) -> None:
        self.user_id = user_id
        self.lesson_id = lesson_id

    def __repr__(self) -> str:
        return f"<Visited {self.id}>"

    @staticmethod
    def add(user_id: str, lesson_id: int) -> None:
        db.session.add(Visited(user_id, lesson_id))
        db.session.commit()
