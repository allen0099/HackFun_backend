from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app import db


class Course(db.Model):
    __tablename__: str = "course"

    id: Column = db.Column(db.Integer,
                           primary_key=True)
    belong: Column = db.Column(db.String(15),
                               db.ForeignKey("tab.name"))
    name: Column = db.Column(db.String(50),
                             unique=True,
                             nullable=False)
    description: Column = db.Column(db.Text,
                                    nullable=False)

    lessons: relationship = db.relationship("Lesson",
                                            backref="course",
                                            lazy="dynamic")

    def __repr__(self) -> str:
        return "<Course %r>" % self.name
