from sqlalchemy.orm import relationship

from app import db


class Tab(db.Model):
    __tablename__: str = "tab"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    name: str = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
        index=True
    )

    course: relationship = db.relationship(
        "Course",
        backref="tab",
        lazy="dynamic"
    )

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Tab {self.name}>"
