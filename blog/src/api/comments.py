from flask import Blueprint, jsonify, abort, request
import sqlalchemy
from ..models import Blog, Comment, User, comment_likes_table, comment_likes_table, db
from flask_sqlalchemy import SQLAlchemy
import traceback

bp = Blueprint('comments', __name__, url_prefix='/comments')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    comments = Comment.query.all()  # ORM performs SELECT query
    result = []
    for comment in comments:
        result.append(comment.serialize())  # build list of Comments as dictionaries
    return jsonify(result)  # return JSON response



@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.serialize())


# @bp.route('', methods=['POST'])
# def create():
#     # req body must contain user_id and content
#     if ('user_id' not in request.json
#             or 'content' not in request.json
#             or 'title' not in request.json):
#         return abort(400)
#
#     # user with id of user_id must exist
#     User.query.get_or_404(request.json['user_id'])
#
#     # construct Comment
#     comment = Comment(
#         title=request.json['title'],
#         content=request.json['content'],
#         user_id=request.json['user_id']
#     )
#
#     db.session.add(comment)  # prepare CREATE statement
#     db.session.commit()  # execute CREATE statement
#
#     return jsonify(comment.serialize())
#
#
# @bp.route('/<int:id>', methods=['DELETE'])
# def delete(id: int):
#     comment = Comment.query.get_or_404(id)
#     try:
#         db.session.delete(comment)  # prepare DELETE statement
#         db.session.commit()  # execute DELETE statement
#         return jsonify(True)
#     except:
#         # something went wrong :(
#         return jsonify(False)
#
#
# @bp.route('/<int:id>/liking_users', methods=['GET'])  # decorator takes path and list of HTTP verbs
# def liking_users(id: int):
#     comment = Comment.query.get_or_404(id)
#     liking_users = comment.comment_likes
#     result = []
#     for user in liking_users:
#         result.append(user.serialize())  # build list of Comments as dictionaries
#     return jsonify(result)  # return JSON response
#
#
# # Bonus Task 1: Implement like endpoint
# @bp.route('/<int:id>/like', methods=['POST'])
# def like(id: int):
#     # Verify comment exists
#     Comment.query.get_or_404(id)
#
#     # Check that a user_id is provided abort if not
#     if 'user_id' not in request.json:
#         return abort(400)
#     # Verify user exists
#     User.query.get_or_404(request.json['user_id'])
#
#     stmt = sqlalchemy.insert(comment_likes_table).values(
#         user_id=request.json['user_id'], comment_id=id
#     )
#
#     # add like record to comment_likes_table
#     try:
#         db.session.execute(stmt)
#         db.session.commit()
#     except Exception as exception:
#         return jsonify(False)
#     return jsonify(True)
#
#
# # Bonus Task 2: Implement Unlike endpoint
# @bp.route('/<int:comment_id>/unlike/<int:user_id>', methods=['DELETE'])
# def unlike(comment_id: int, user_id: int):
#     # Check if comment and user exist
#     Comment.query.get_or_404(comment_id)
#     User.query.get_or_404(user_id)
#     # Deletes record from comment_likes_table intermediate table
#     stmt = sqlalchemy.delete(comment_likes_table).where(sqlalchemy.and_(
#         comment_likes_table.c.user_id == user_id,
#         comment_likes_table.c.comment_id == comment_id)
#     )
#     # Remove like record from likes table
#     try:
#         db.session.execute(stmt)
#         db.session.commit()
#     except Exception as exception:
#         return jsonify(False)
#     return jsonify(True)