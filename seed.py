"""
Populate blog database with fake data using the SQLAlchemy ORM.
"""

import random
import string
import hashlib
import secrets
from faker import Faker
from blog.src.models import User, Blog, Comment, blog_likes_table, comment_likes_table, db
from blog.src import create_app

USER_COUNT = 50
BLOG_COUNT = 150
COMMENT_COUNT = 300
BLOG_LIKE_COUNT = 400
COMMENT_LIKE_COUNT = 500

assert BLOG_LIKE_COUNT <= (USER_COUNT * BLOG_COUNT)


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(blog_likes_table.delete())
    Blog.query.delete()
    User.query.delete()
    # TODO: Untested addition
    Comment.query.delete()
    db.session.execute(comment_likes_table.delete())
    db.session.commit()
    # TODO: restart identity/alter sequence _ start 1


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    last_user = insert_users(fake)
    last_blog = insert_blogs(fake, last_user)
    insert_likes(last_blog, last_user)
    last_comment = insert_comments(fake, last_blog, last_user)
    insert_comment_likes(last_comment, last_user)


def insert_comments(fake, last_blog, last_user):
    last_comment = None  # save last comment
    for _ in range(COMMENT_COUNT):
        count = 1
        if count % 19 == 0:
            last_comment = Comment(
                content=fake.sentence(),
                blog_id=random.randint(last_blog.id - BLOG_COUNT + 1, last_blog.id)
            )
        else:
            last_comment = Comment(
                content=fake.sentence(),
                blog_id=random.randint(last_blog.id - BLOG_COUNT + 1, last_blog.id),
                user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
            )
        db.session.add(last_comment)
        count = random.randint(1, 20)
    # insert blogs
    db.session.commit()
    return last_comment


def insert_comment_likes(last_comment, last_user):
    user_comment_pairs = set()
    while len(user_comment_pairs) < COMMENT_LIKE_COUNT:

        candidate = (
            random.randint(last_user.id - USER_COUNT + 1, last_user.id),
            random.randint(last_comment.id - COMMENT_COUNT + 1, last_comment.id)
        )

        if candidate in user_comment_pairs:
            continue  # pairs must be unique

        user_comment_pairs.add(candidate)
    new_likes = [{"user_id": pair[0], "comment_id": pair[1]} for pair in list(user_comment_pairs)]
    insert_likes_query = comment_likes_table.insert().values(new_likes)
    db.session.execute(insert_likes_query)
    # insert likes
    db.session.commit()


def insert_likes(last_blog, last_user):
    user_blog_pairs = set()
    while len(user_blog_pairs) < BLOG_LIKE_COUNT:

        candidate = (
            random.randint(last_user.id - USER_COUNT + 1, last_user.id),
            random.randint(last_blog.id - BLOG_COUNT + 1, last_blog.id)
        )

        if candidate in user_blog_pairs:
            continue  # pairs must be unique

        user_blog_pairs.add(candidate)
    new_likes = [{"user_id": pair[0], "blog_id": pair[1]} for pair in list(user_blog_pairs)]
    insert_likes_query = blog_likes_table.insert().values(new_likes)
    db.session.execute(insert_likes_query)
    # insert likes
    db.session.commit()


def insert_blogs(fake, last_user):
    last_blog = None  # save last blog
    for _ in range(BLOG_COUNT):
        last_blog = Blog(
            title=fake.sentence(),
            content=fake.paragraph(),
            user_id=random.randint(last_user.id - USER_COUNT + 1, last_user.id)
        )
        db.session.add(last_blog)
    # insert blogs
    db.session.commit()
    return last_blog


def insert_users(fake):
    last_user = None  # save last user
    count = 1
    for _ in range(USER_COUNT):
        first_name = fake.unique.first_name()
        if count % 9 == 0:
            last_user = User(
                username=first_name.lower() + str(random.randint(1, 150)),
                password=random_passhash()
            )
        elif count % 3 == 0:
            last_user = User(
                username=first_name.lower() + str(random.randint(1, 150)),
                password=random_passhash(),
                fullname=first_name + ' ' + fake.name(),
                email=first_name.lower() + fake.unique.email()
            )
        else:
            last_user = User(
                username=first_name.lower() + str(random.randint(1, 150)),
                password=random_passhash(),
                email=first_name.lower() + fake.unique.email()
            )
        db.session.add(last_user)
        count = random.randint(1, 10)
    # insert users
    db.session.commit()
    return last_user


# run script
main()
