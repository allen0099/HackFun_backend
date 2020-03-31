from sqlalchemy import Column

from app import db


class Choose(db.Model):
    __tablename__: str = "choose"

    id: Column = db.Column(
        db.Integer,
        primary_key=True
    )
    belong_to: Column = db.Column(
        db.String(64),
        db.ForeignKey("practice.uuid")
    )
    choose_count: Column = db.Column(
        db.Integer()
    )
    can_multiple: Column = db.Column(
        db.Boolean
    )
    ans: Column = db.Column(
        db.Integer,
        default=10000000000
    )
    chosen_1: Column = db.Column(
        db.Text
    )
    chosen_2: Column = db.Column(
        db.Text
    )
    chosen_3: Column = db.Column(
        db.Text
    )
    chosen_4: Column = db.Column(
        db.Text
    )
    chosen_5: Column = db.Column(
        db.Text
    )
    chosen_6: Column = db.Column(
        db.Text
    )
    chosen_7: Column = db.Column(
        db.Text
    )
    chosen_8: Column = db.Column(
        db.Text
    )
    chosen_9: Column = db.Column(
        db.Text
    )
    chosen_10: Column = db.Column(
        db.Text
    )

    def __repr__(self) -> str:
        return "<Choose %r>" % self.id
