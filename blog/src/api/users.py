from flask import Blueprint, jsonify, abort, request
import sqlalchemy
from ..models import Blog, User, blog_likes_table, comment_likes_table, db
from flask_sqlalchemy import SQLAlchemy

import traceback
import hashlib
import secrets

bp = Blueprint('users', __name__, url_prefix='/users')


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = User.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)

    print('>>> ', str(request.json['username']))
    # The username value must be at least 3 characters long. Else, abort 400
    if len(request.json['username']) < 3:
        return abort(400)
    # The password value must be at least 8 characters long. Else, abort 400
    if len(request.json['password']) < 8:
        return abort(400)
    # username must not exist
    if bool(User.query.filter_by(username=request.json['username']).first()):
        return abort(400)

    # construct Blog
    u = User(
        username=request.json['username'],
        # hash and salt password before storage
        password=scramble(request.json['password'])
    )

    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(u.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):
    # Get the User matching the route parameter id
    u = User.query.get_or_404(id)

    # If a username is provided in the request body, set the User's username property to this value
    if 'username' in request.json:
        if len(request.json['username']) < 3:
            return abort(400)
        u.username = request.json['username']
    # If a password is provided in the request body, set the User's password property to a scrambled version of this value
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        # hash and salt password before storage
        u.password = scramble(request.json['password'])

    db.session.commit()  # execute CREATE statement

    return jsonify(u.serialize())


# decorator takes path and list of HTTP verbs
@bp.route('/<int:id>/liked_blogs', methods=['GET'])
def liked_blogs(id: int):
    u = User.query.get_or_404(id)
    user_liked_blogs = u.liked_blogs
    result = []
    for t in user_liked_blogs:
        result.append(t.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


# Bonus Task 1: Implement like endpoint TODO: Should be implemented in /blogs/:blog
@bp.route('/<int:id>/like', methods=['POST'])
def like(id: int):
    # check that a blog_id is provided abort if not
    if 'blog_id' not in request.json:
        return abort(400)
    u = User.query.get_or_404(id)
    liked_blog = Blog.query.get_or_404(request.json['blog_id'])
    stmt = sqlalchemy.insert(blog_likes_table).values(
        user_id=id, blog_id=request.json['blog_id'])

    # add like record to likes table
    try:
        db.session.execute(stmt)
        db.session.commit()
    except Exception as exception:
        return jsonify(False)
    return jsonify(True)


# Bonus Task 2: Implement Unlike endpoint
@bp.route('/<int:user_id>/unlike/<int:blog_id>', methods=['DELETE'])
def unlike(user_id: int, blog_id: int):
    # Check if user and blog exist
    User.query.get_or_404(user_id)
    Blog.query.get_or_404(blog_id)

    stmt = sqlalchemy.delete(blog_likes_table).where(sqlalchemy.and_(
        blog_likes_table.c.user_id == user_id,
        blog_likes_table.c.blog_id == blog_id)
    )

    # remove like record from likes table
    try:
        db.session.execute(stmt)
        db.session.commit()
    except Exception as exception:
        return jsonify(False)
    return jsonify(True)
