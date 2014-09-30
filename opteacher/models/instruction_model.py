# -*- coding: utf-8 -*-

from opteacher.ext import db


class InstructionModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    learning_models = db.relationship('LearningModel', lazy='dynamic',
                                      backref='instruction_model')


class LearningModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    instruction_model_id = db.Column(db.Integer,
                                     db.ForeignKey('instruction_model.id'))
    name = db.Column(db.String(40), nullable=False)
    steps = db.relationship('LearningStep', backref='learning_model')
    count = db.Column(db.Integer, nullable=False, default=0)


class LearningStep(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    learning_model_id = db.Column(db.Integer,
                                  db.ForeignKey('learning_model.id'))
    name = db.Column(db.String(40), nullable=False)
    activities = db.relationship('LearningActivity', backref='learning_step')


class LearningActivity(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    learning_step_id = db.Column(db.Integer,
                                 db.ForeignKey('learning_step.id'))
    name = db.Column(db.String(40), nullable=False)
