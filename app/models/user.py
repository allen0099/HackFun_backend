from __future__ import annotations

from typing import Union

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__: str = "users"

    id: str = db.Column(
        db.String(30),
        primary_key=True
    )
    name: str = db.Column(
        db.Text
    )
    email: str = db.Column(
        db.String(255),
        unique=True
    )
    profile_pic: str = db.Column(
        db.Text
    )

    def __init__(
            self,
            id_: str,
            name: str,
            email: str,
            profile_pic: str
    ) -> None:
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def __repr__(self) -> str:
        return f"<User {self.id}>"

    @staticmethod
    def update(user_id: str, name: str, email: str, pic: str) -> Union[str, None]:
        user = User.get(user_id)
        if user is None:
            return "UserNotFound"
        User.query.filter_by(id=user_id) \
            .update(dict(name=name,
                         email=email,
                         profile_pic=pic))
        db.session.commit()

    @staticmethod
    def add(user_id: str, name: str, email: str, pic: str) -> Union[None, str]:
        check = User.query.filter_by(id=user_id).first()
        if check is None:
            db.session.add(User(user_id,
                                name,
                                email,
                                pic))
            db.session.commit()
            return user_id
        else:
            return check.id

    @staticmethod
    def get(uid: str) -> Union[User, None]:
        user = User.query.filter_by(id=uid).first()
        if user is None:
            return None
        return User(
            id_=user.id,
            name=user.name,
            email=user.email,
            profile_pic=user.profile_pic
        )
