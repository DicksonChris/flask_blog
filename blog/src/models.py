import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Reference:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    joined = db.Column(
        'joined', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    fullname = db.Column(db.String(60))
    email = db.Column(db.String(128), unique=True)

    blogs = db.relationship('Blog', backref='user', cascade="all,delete")
    comments = db.relationship('Comment', backref='user', cascade="all,delete")

    def __init__(self, username: str, password: str, fullname: str = None, email: str = None):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email

    # TODO: Add more attributes to serialize
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'joined': self.joined.isoformat(),
            'fullname': self.fullname,
            'email': self.email
        }


blog_likes_table = db.Table(
    'blog_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'blog_id', db.Integer,
        db.ForeignKey('blogs.id'),
        primary_key=True
    ),

    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    blog_likes = db.relationship(
        'User', secondary=blog_likes_table,
        lazy='subquery',
        backref=db.backref('liked_blogs', lazy=True)
    )

    def __init__(self, title: str, content: str, user_id: int):
        self.title = title
        self.content = content
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }


comment_likes_table = db.Table(
    'comment_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'comment_id', db.Integer,
        db.ForeignKey('comment.id'),
        primary_key=True
    ),

    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content: str, blog_id: int, user_id: int):
        self.content = content
        self.blog_id = blog_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'blog_id': self.blog_id,
            'user_id': self.user_id
        }
