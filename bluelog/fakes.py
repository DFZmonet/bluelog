# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog.extensions import db
from bluelog.models import Admin, Category, Post, Comment, Link

fake = Faker()


def fake_admin():
    admin = Admin(
        username='wmm',
        blog_title='520wmb',
        blog_sub_title="希望和宝贝长长久久❤️",
        name='Mima Kirigoe',
        about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...'
    )
    admin.set_password('wkq')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=1):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=1):
    # for i in range(count):
    #     post = Post(
    #         title=fake.sentence(),
    #         body=fake.text(2000),
    #         category=Category.query.get(random.randint(1, Category.query.count())),
    #         timestamp=fake.date_time_this_year()
    #     )
    post = Post(
        title='宝贝生日快乐🎂',
        body='喜欢宝贝的每一天都很幸福',
        category=Category.query.get(random.randint(1, Category.query.count())),
        timestamp=fake.date_time_this_year()
    )
    db.session.add(post)
    db.session.commit()


def fake_comments(count=1):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # unreviewed comments
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # from admin
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    weibo = Link(name='Weibo', url='https://weibo.com/u/6269655963')
    # facebook = Link(name='Facebook', url='#')
    # linkedin = Link(name='LinkedIn', url='#')
    # google = Link(name='Google+', url='#')
    # db.session.add_all([twitter, facebook, linkedin, google])
    db.session.add_all([weibo])
    db.session.commit()
