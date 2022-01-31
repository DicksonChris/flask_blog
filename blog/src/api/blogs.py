from flask import Blueprint, jsonify, abort, request
import sqlalchemy
from ..models import Blog, User, blog_likes_table, comment_likes_table, db
from flask_sqlalchemy import SQLAlchemy
import traceback

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    blogs = Blog.query.all()  # ORM performs SELECT query
    result = []
    for blog in blogs:
        result.append(blog.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    blog = Blog.query.get_or_404(id)
    return jsonify(blog.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if ('user_id' not in request.json
            or 'content' not in request.json
            or 'title' not in request.json):
        return abort(400)

    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])

    # construct Blog
    blog = Blog(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id']
    )

    db.session.add(blog)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(blog.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    blog = Blog.query.get_or_404(id)
    try:
        db.session.delete(blog)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/liking_users', methods=['GET'])  # decorator takes path and list of HTTP verbs
def liking_users(id: int):
    blog = Blog.query.get_or_404(id)
    liking_users = blog.blog_likes
    result = []
    for user in liking_users:
        result.append(user.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


# Bonus Task 1: Implement like endpoint TODO: Should be implemented in /blogs/:blog
@bp.route('/<int:id>/like', methods=['POST']) # TODO: PUT instead of POST?
def like(id: int):
    # check that a blog_id is provided abort if not
    if 'user_id' not in request.json:
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
