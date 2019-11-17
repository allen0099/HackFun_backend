from __future__ import annotations

import uuid
from typing import Union

from flask_login import UserMixin

from app import db


def generate_uuid(prefix: str = "") -> str:
    return prefix + str(uuid.uuid4())


class Tab(db.Model):
    __tablename__ = "tab"

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(15),
                     unique=True,
                     nullable=False)

    course = db.relationship("Course",
                             backref="tab",
                             lazy="dynamic")

    def __repr__(self):
        return "<Tab %r>" % self.tab


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer,
                   primary_key=True)
    belong = db.Column(db.String(15),
                       db.ForeignKey("tab.name"))
    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    description = db.Column(db.Text,
                            nullable=False)

    lessons = db.relationship("Lesson",
                              backref="course",
                              lazy="dynamic")

    def __repr__(self):
        return "<Course %r>" % self.name


class Lesson(db.Model):
    __tablename__ = "lesson"

    id = db.Column(db.Integer,
                   primary_key=True)
    uuid = db.Column(db.String(64),
                     default=generate_uuid("lesson-"),
                     unique=True,
                     nullable=False)
    belong = db.Column(db.String(50),
                       db.ForeignKey("course.name"))
    name = db.Column(db.String(255),
                     unique=True,
                     nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.Text)

    practices = db.relationship("Practice",
                                backref="lesson",
                                lazy="dynamic")

    def __repr__(self):
        return "<Lesson %r>" % self.name


class Practice(db.Model):
    __tablename__ = "practice"

    id = db.Column(db.Integer,
                   primary_key=True)
    uuid = db.Column(db.String(64),
                     default=generate_uuid(),
                     unique=True,
                     nullable=False)
    belong = db.Column(db.Integer,
                       db.ForeignKey("lesson.id"))
    name = db.Column(db.Text,
                     nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20))

    hint = db.relationship("Hint",
                           backref="practice",
                           lazy="dynamic")

    choose = db.relationship("Choose",
                             backref="practice",
                             lazy="dynamic")

    docker = db.relationship("Docker",
                             backref="practice",
                             lazy="dynamic")

    def __repr__(self):
        return "<Practice %r>" % self.name


class Hint(db.Model):
    __tablename__ = "hint"

    id = db.Column(db.Integer,
                   primary_key=True)
    belong = db.Column(db.String(64),
                       db.ForeignKey("practice.uuid"))
    item = db.Column(db.String(20),
                     nullable=False)
    description = db.Column(db.Text,
                            nullable=False)

    def __repr__(self):
        return "<Hint %r>" % self.name


class Choose(db.Model):
    __tablename__ = "choose"

    id = db.Column(db.Integer,
                   primary_key=True)
    belong_to = db.Column(db.String(64),
                          db.ForeignKey("practice.uuid"))
    choose_count = db.Column(db.Integer())
    can_multiple = db.Column(db.Boolean)
    ans = db.Column(db.Integer,
                    default=10000000000)
    chosen_1 = db.Column(db.Text)
    chosen_2 = db.Column(db.Text)
    chosen_3 = db.Column(db.Text)
    chosen_4 = db.Column(db.Text)
    chosen_5 = db.Column(db.Text)
    chosen_6 = db.Column(db.Text)
    chosen_7 = db.Column(db.Text)
    chosen_8 = db.Column(db.Text)
    chosen_9 = db.Column(db.Text)
    chosen_10 = db.Column(db.Text)

    def __repr__(self):
        return "<Choose %r>" % self.id


class Docker(db.Model):
    __tablename__ = "docker"

    id = db.Column(db.Integer,
                   primary_key=True)
    belong_to = db.Column(db.String(64),
                          db.ForeignKey("practice.uuid"))
    url = db.Column(db.Text)
    flag = db.Column(db.Text)
    image = db.Column(db.Text)

    def __repr__(self):
        return "<Docker %r>" % self.id


class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, id_: str, name: str, email: str, profile_pic: str) -> None:
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    id: str = db.Column(
        db.String(30),
        primary_key=True
    )
    name: str = db.Column(
        db.String(255)
    )
    email: str = db.Column(
        db.String(255),
        unique=True
    )
    profile_pic: str = db.Column(
        db.String(255)
    )

    def __repr__(self):
        return f"<User {self.id}>"

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile pic": self.profile_pic
        }

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
