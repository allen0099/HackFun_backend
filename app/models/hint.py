from sqlalchemy import Column

from app import db


class Hint(db.Model):
    __tablename__: str = "hint"

    id: Column = db.Column(db.Integer,
                           primary_key=True)
    belong: Column = db.Column(db.String(64),
                               db.ForeignKey("practice.uuid"))
    item: Column = db.Column(db.String(20),
                             nullable=False)
    description: Column = db.Column(db.Text,
                                    nullable=False)

    def __repr__(self) -> str:
        return "<Hint %r>" % self.name
