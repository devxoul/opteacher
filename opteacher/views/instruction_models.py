# -*- coding: utf-8 -*-

import random

from flask import Blueprint, render_template

from opteacher.models.instruction_model import InstructionModel


mod = Blueprint('instruction_models', __name__,
                url_prefix='/instruction_models')


@mod.route('/')
def index():
    return 'Hi'


@mod.route('/<string:subject>')
def subject(subject):
    instruction = InstructionModel.query.filter_by(subject=subject).first()
    learning = random.choice(instruction.learning_models)
    return render_template('instruction_models.html',
                           instruction_model=instruction,
                           learning_model=learning)


@mod.route('/<string:subject>', methods=['POST'])
def validate(subject):
    pass
