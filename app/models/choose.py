from sqlalchemy.orm import relationship

from app import db


class Choose(db.Model):
    __tablename__: str = "choose"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    practice_id: int = db.Column(
        db.Integer,
        db.ForeignKey("practice.id")
    )
    statement: str = db.Column(
        db.Text,
        nullable=False
    )

    option: relationship = db.relationship(
        "Option",
        backref="choose",
        lazy="dynamic"
    )

    def __init__(self, belong, statement) -> None:
        self.belong = belong
        self.statement = statement

    def __repr__(self) -> str:
        return f"<Choose {self.id}>"
