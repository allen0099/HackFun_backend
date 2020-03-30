from sqlalchemy import Column
from sqlalchemy.orm import relationship

from app import db
from app.models.uuid import generate


class Practice(db.Model):
    __tablename__: str = "practice"

    id: Column = db.Column(db.Integer,
                           primary_key=True)
    uuid: Column = db.Column(db.String(64),
                             default=generate(),
                             unique=True,
                             nullable=False)
    belong: Column = db.Column(db.Integer,
                               db.ForeignKey("lesson.id"))
    name: Column = db.Column(db.Text,
                             nullable=False)
    description: Column = db.Column(db.Text)
    type: Column = db.Column(db.String(20))

    hint: relationship = db.relationship("Hint",
                                         backref="practice",
                                         lazy="dynamic")

    choose: relationship = db.relationship("Choose",
                                           backref="practice",
                                           lazy="dynamic")

    docker: relationship = db.relationship("Docker",
                                           backref="practice",
                                           lazy="dynamic")

    def __repr__(self) -> str:
        return "<Practice %r>" % self.name
