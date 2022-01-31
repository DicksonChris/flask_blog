from flask import Blueprint, jsonify, abort, request
from ..models import Blog, User, db

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    blogs = Blog.query.all()  # ORM performs SELECT query
    result = []
    for t in blogs:
        result.append(t.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Blog.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'content' not in request.json:
        return abort(400)

    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])

    # construct Blog
    t = Blog(
        user_id=request.json['user_id'],
        content=request.json['content']
    )

    db.session.add(t)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(t.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Blog.query.get_or_404(id)
    try:
        db.session.delete(t)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/liking_users', methods=['GET'])  # decorator takes path and list of HTTP verbs
def liking_users(id: int):
    t = Blog.query.get_or_404(id)
    liking_users = t.likes
    result = []
    for u in liking_users:
        result.append(u.serialize())  # build list of Blogs as dictionaries
    return jsonify(result)  # return JSON response