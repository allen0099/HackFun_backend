from app import db


class Knowledge(db.Model):
    __tablename__: str = "knowledge"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    belong: str = db.Column(
        db.String(50),
        db.ForeignKey("course.name")
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )

    def __init__(self, belong, desc) -> None:
        self.belong = belong
        self.desc = desc

    def __repr__(self) -> str:
        return f"<Knowledge {self.id}>"
