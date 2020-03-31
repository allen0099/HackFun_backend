from sqlalchemy import Column

from app import db


class Docker(db.Model):
    __tablename__: str = "docker"

    id: Column = db.Column(
        db.Integer,
        primary_key=True
    )
    belong_to: Column = db.Column(
        db.String(64),
        db.ForeignKey("practice.uuid")
    )
    url: Column = db.Column(
        db.Text
    )
    flag: Column = db.Column(
        db.Text
    )
    image: Column = db.Column(
        db.Text
    )

    def __repr__(self) -> str:
        return "<Docker %r>" % self.id
