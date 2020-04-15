from app import db


class Option(db.Model):
    __tablename__: str = "option"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: int = db.Column(
        db.Integer,
        db.ForeignKey("choose.id")
    )
    statement: str = db.Column(
        db.Text,
        nullable=False
    )
    is_ans: bool = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(self, belong, statement, is_ans) -> None:
        self.belong = belong
        self.statement = statement
        self.is_ans = is_ans

    def __repr__(self) -> str:
        return f"<Option {self.id}>"
