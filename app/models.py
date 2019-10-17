from __future__ import annotations

import uuid
from typing import Union

from flask_login import UserMixin

from app import db


def generateUUID(prefix: str = "") -> str:
    return prefix + str(uuid.uuid4())


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(255),
                     unique=True)
    info = db.Column(db.Text)
    # backref means you can use Class.backref to find Course
    classes = db.relationship("Class",
                              backref="course",
                              lazy="dynamic")

    def __repr__(self):
        return "<Course %r>" % self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "info": self.info
        }


class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer,
                   primary_key=True)
    # belong to which course
    belong = db.Column(db.String(255),
                       db.ForeignKey("courses.name"))
    name = db.Column(db.String(255),
                     unique=True)
    info = db.Column(db.Text)

    # provide backref for topic
    topics = db.relationship("Topic",
                             backref="class",
                             lazy="dynamic")

    def __repr__(self):
        return "<Class %r>" % self.name

    def to_dict(self):
        return {
            "name": self.name,
            "info": self.info,
            "topics": {
                "topic_count": len(self.topics.all()),
                "topics_uuid": [Topic.get_uuid(uuid) for uuid in self.topics.all()]
            }
        }


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer,
                   primary_key=True)
    uuid = db.Column(db.String(64),
                     default=generateUUID("topic-"),
                     unique=True,
                     nullable=False)
    # belong to which class
    belong = db.Column(db.Integer,
                       db.ForeignKey("classes.id"))
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    type = db.Column(db.String(20))

    # provide backref for types
    classes = db.relationship("TopicChoose",
                              backref="topic",
                              lazy="dynamic")

    def __repr__(self):
        return "<Topic %r>" % self.name

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description
        }

    def get_uuid(self):
        return self.uuid


class TopicChoose(db.Model):
    __tablename__ = "topic_choose"

    id = db.Column(db.Integer,
                   primary_key=True)
    # belong to which topic
    belong_to = db.Column(db.Integer,
                          db.ForeignKey("topics.id"))
    choose_count = db.Column(db.Integer())
    can_multiple = db.Column(db.Boolean)
    ans = db.Column(db.Text)
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
        return "<Topic_Choose %r>" % self.id


class TopicDocker(db.Model):
    __tablename__ = "topic_docker"

    id = db.Column(db.Integer,
                   primary_key=True)
    # belong to which topic
    belong_to = db.Column(db.Integer,
                          db.ForeignKey("topics.id"))
    docker_url = db.Column(db.Text)
    docker_flag = db.Column(db.Text)
    docker_image = db.Column(db.Text)

    def __repr__(self):
        return "<Topic %r>" % self.id


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
