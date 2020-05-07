from sqlalchemy.orm import relationship

from app import db


class Course(db.Model):
    __tablename__: str = "course"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    tab_id: int = db.Column(
        db.Integer,
        db.ForeignKey("tab.id")
    )
    name: str = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        index=True
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )

    lessons: relationship = db.relationship(
        "Lesson",
        backref="course",
        lazy="dynamic"
    )
    knowledge: relationship = db.relationship(
        "Knowledge",
        backref="course",
        lazy="dynamic"
    )

    def __init__(
            self,
            belong: str,
            name: str,
            desc: str
    ) -> None:
        self.belong = belong
        self.name = name
        self.desc = desc

    def __repr__(self) -> str:
        return f"<Course {self.name}>"
