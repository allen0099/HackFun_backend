from app import db


# What are you looking for?
class Flag(db.Model):
    __tablename__: str = "flag"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    # belong
    docker: id = db.Column(
        db.Integer,
        db.ForeignKey("docker.id")
    )
    flag: str = db.Column(
        db.Text,
        nullable=False
    )

    def __init__(self, flag, question=None, docker=None) -> None:
        self.flag = flag
        self.question = question
        self.docker = docker

    def __repr__(self) -> str:
        return f"<Flag {self.id}>"
