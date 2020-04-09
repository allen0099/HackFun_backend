from app import db


class Hint(db.Model):
    __tablename__: str = "hint"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: int = db.Column(
        db.Integer,
        db.ForeignKey("practice.id")
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )

    def __init__(self, belong: int, desc: str) -> None:
        self.belong = belong
        self.desc = desc

    def __repr__(self) -> str:
        return f"<Hint {self.id}>"
