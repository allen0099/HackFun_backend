from sqlalchemy import Column

from app import db


class Options(db.Model):
    __tablename__ = "options"

    id: Column = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: Column = db.Column(
        db.Integer,
        db.ForeignKey("question.id")
    )
    desc: Column = db.Column(
        db.Text,
        nullable=False
    )
    ans: Column = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(self, belong, desc, ans=None) -> None:
        self.belong = belong
        self.desc = desc
        self.ans = ans

    def __repr__(self) -> str:
        return "<Options %r>" % self.desc
