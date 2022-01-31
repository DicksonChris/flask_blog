from flask import Blueprint, jsonify, abort, request
import sqlalchemy
from ..models import Blog, User, blog_likes_table, comment_likes_table, db

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
    for user in users:
        result.append(user.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


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
    user = User(
        username=request.json['username'],
        # hash and salt password before storage
        password=scramble(request.json['password']),
        fullname=request.json['fullname'],
        email=request.json['email']
    )

    db.session.add(user)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(user.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):
    # Get the User matching the route parameter id
    user = User.query.get_or_404(id)

    # If a username is provided in the request body, set the User's username property to this value
    if 'username' in request.json:
        if len(request.json['username']) < 3:
            return abort(400)
        user.username = request.json['username']
    # If a password is provided in the request body, set the User's password property to a scrambled version of this value
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        # hash and salt password before storage
        user.password = scramble(request.json['password'])
    # Handle fullname
    if 'fullname' in request.json:
        # TODO fullname can't be only whitespace
        if len(request.json['fullname']) == 0:
            user.fullname = None
        user.fullname = request.json['fullname']
    # Handle email
    # TODO verify email structure
    if 'email' in request.json:
        user.email = request.json['email']

    db.session.commit()  # execute CREATE statement

    return jsonify(user.serialize())


# decorator takes path and list of HTTP verbs
@bp.route('/<int:id>/liked_blogs', methods=['GET'])
def liked_blogs(id: int):
    user = User.query.get_or_404(id)
    user_liked_blogs = user.liked_blogs
    result = []
    for blog in user_liked_blogs:
        result.append(blog.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response
