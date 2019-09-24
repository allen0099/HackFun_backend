from typing import Union

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    def __init__(self, id_: str, name: str, email: str, profile_pic: str) -> None:
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    id: str = db.Column(db.CHAR(200), nullable=False, primary_key=True)
    name: str = db.Column(db.CHAR(200), nullable=False, unique=False)
    email: str = db.Column(db.CHAR(200), nullable=False, unique=True)
    profile_pic: str = db.Column(db.CHAR(200), nullable=False, unique=False)

    def __repr__(self):
        return f"<User {self.id}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile pic": self.profile_pic
        }

    @staticmethod
    def add_user(user_id: str, name: str, email: str, pic: str) -> None:
        check = User.query.filter_by(id=user_id).first()
        if check is None:
            db.session.add(User(user_id, name, email, pic))
            db.session.commit()
        return None

    @staticmethod
    def get_user(uid) -> Union[str, None]:
        print("getting id")
        user = User.query.filter_by(id=uid).first()
        if user is None:
            return None
        user = User.to_dict(user)
        user = User(
            id_=user["id"], name=user["name"], email=user["email"], profile_pic=user["profile pic"]
        )
        return user

    @staticmethod
    def search(uid: str) -> str:
        # TODO implement function
        pass


class Course(db.Model):
    __tablename__ = "course"

    id: int = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name: str = db.Column(db.CHAR(255), nullable=False, unique=True)
    info: str = db.Column(db.TEXT, nullable=True, unique=False)

    def __repr__(self) -> str:
        return "<Course %r>" % self.name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info
        }

    @staticmethod
    def add(name: str, info: str, cid: int = None) -> int:
        if cid is not None:
            db.session.add(Course(id=cid, name=name, info=info))
        else:
            db.session.add(Course(name=name, info=info))
        db.session.commit()
        return Course.search(name)[0]["id"]

    @staticmethod
    def search(item: str = None) -> Union[list, None]:
        if item is None:
            course = Course.query.all()
        else:
            course = Course.query.filter_by(name=item).all()
        course_list = [Course.to_dict(cs) for cs in course]
        if len(course_list) == 0:
            return None
        return course_list


class Class(db.Model):
    __tablename__ = "class"

    id: int = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    course: str = db.Column(db.TEXT, nullable=False, unique=False)
    name: str = db.Column(db.TEXT, nullable=False, unique=False)
    info: str = db.Column(db.TEXT, nullable=False, unique=False)

    def __repr__(self) -> str:
        return "<Class %r>" % self.name

    def to_dict(self):
        return {
            "id": self.id,
            "course": self.course,
            "name": self.name,
            "info": self.info
        }

    @staticmethod
    def search(course: str) -> Union[list, None]:
        c = Course.search(course)
        if c is None:
            return None
        css = Class.query.filter_by(course=course).all()
        css = [Class.to_dict(cs) for cs in css]
        return css


class Topic(db.Model):
    __tablename__ = "topic"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    belong_to = db.Column(db.TEXT, nullable=False, unique=False)
    name = db.Column(db.TEXT, nullable=False, unique=False)
    description = db.Column(db.TEXT, nullable=False, unique=False)
    type = db.Column(db.TEXT, nullable=False, unique=False)

    def __repr__(self):
        return "<Topic %r>" % self.name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "belong to": self.belong_to,
            "name": self.name,
            "description": self.description,
            "type": self.type
        }

    @staticmethod
    def search(tid: int = None, course: str = None) -> Union[list, dict, None]:
        if tid is not None:
            topic = Topic.query.filter_by(id=tid).first()
            if topic is None:
                return None
            return topic.to_dict()
        if course is not None:
            topic = Topic.query.filter_by(belong_to=course).all()
            if not topic:
                return None
            return [Topic.to_dict(cs) for cs in topic]

        # none of above triggered, return all query
        topic = Topic.query.all()
        return [Topic.to_dict(cs) for cs in topic]
