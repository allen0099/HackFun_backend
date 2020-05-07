from app import db


class Knowledge(db.Model):
    __tablename__: str = "knowledge"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    course_id: int = db.Column(
        db.Integer,
        db.ForeignKey("course.id")
    )
    desc: str = db.Column(
        db.Text,
        nullable=False
    )
    url: str = db.Column(
        db.Text
    )

    def __init__(self, belong, desc, url=None) -> None:
        self.belong = belong
        self.desc = desc
        self.url = url

    def __repr__(self) -> str:
        return f"<Knowledge {self.id}>"
