# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
