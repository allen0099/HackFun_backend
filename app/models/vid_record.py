from datetime import datetime

from app import db


class VidRecord(db.Model):
    __tablename__: str = "vid_record"

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
    progress: int = db.Column(
        db.Integer,
        nullable=False
    )
    time: int = db.Column(
        db.Integer,
        nullable=False
    )
    create_time: datetime = db.Column(
        db.TIMESTAMP(),
        server_default=db.func.now()
    )
    update_time: datetime = db.Column(
        db.DATETIME,
        # some trick server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __init__(self,
                 user_id: str,
                 lesson_id: int,
                 progress: int,
                 time: int) -> None:
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.progress = progress
        self.time = time

    def __repr__(self) -> str:
        return f"<Video Record {self.id}>"

    @staticmethod
    def add(user_id: str, lesson_id: int, progress: int, time: int) -> None:
        db.session.add(VidRecord(user_id, lesson_id, progress, time))
        db.session.commit()

    def update(self, progress: int, time: int) -> None:
        self.progress = progress
        self.time = time
        db.session.commit()
