# -*- coding: utf-8 -*-

from flask import Blueprint, g, render_template

import random

mod = Blueprint('instruction_models', __name__,
                url_prefix='/instruction_models')


@mod.route('/<string:subject>')
def index(subject):
    instruction_model = g.instruction_models.get(subject)
    random_model = random.choice(instruction_model.learning_models)
    return render_template('instruction_models.html',
                           subject=instruction_model.name,
                           learning_model=random_model)
