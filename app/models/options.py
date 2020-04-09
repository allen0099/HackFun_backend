from app import db


class Options(db.Model):
    __tablename__: str = "options"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: int = db.Column(
        db.Integer,
        db.ForeignKey("question.id")
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )
    ans: bool = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(self, belong, desc, ans) -> None:
        self.belong = belong
        self.desc = desc
        self.ans = ans

    def __repr__(self) -> str:
        return f"<Options {self.id}>"
