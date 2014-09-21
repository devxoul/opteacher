# -*- coding: utf-8 -*-

import random

from flask import Blueprint, render_template, request

from werkzeug.exceptions import NotFound

from opteacher.models.instruction_model import InstructionModel, LearningModel


mod = Blueprint('instruction_models', __name__,
                url_prefix='/instruction_models')


@mod.route('/')
def index():
    instruction_models = InstructionModel.query.all()
    return render_template('instruction_models/index.html',
                           instruction_models=instruction_models)


@mod.route('/<string:subject>')
def quiz(subject):
    instruction = InstructionModel.query.filter_by(subject=subject).first()
    if not instruction:
        raise NotFound()

    learning = random.choice(instruction.learning_models)

    blank_step_ids = []
    blank_activity_ids = []

    for step in learning.steps:
        if random.getrandbits(1):
            blank_step_ids.append(str(step.id))
        for activity in step.activities:
            if random.getrandbits(1):
                blank_activity_ids.append(str(activity.id))

    depth = 1
    for step in learning.steps:
        if len(step.activities):
            depth = 2
            break

    return render_template('instruction_models/quiz.html',
                           instruction_model=instruction,
                           learning_model=learning,
                           blank_step_ids=blank_step_ids,
                           blank_activity_ids=blank_activity_ids,
                           input_steps=None,
                           input_activities=None,
                           depth=depth)


@mod.route('/<string:subject>', methods=['POST'])
def validate(subject):
    form = request.form

    instruction = InstructionModel.query.filter_by(subject=subject).first()
    if not instruction:
        raise NotFound()

    learning_model_id = form.get('learning_model_id')
    if not learning_model_id:
        raise NotFound()
    learning = LearningModel.query.get_or_404(learning_model_id)

    input_steps = {}
    input_activities = {}

    for k, v in request.form.iteritems():
        if k.startswith('step-'):
            step_id = k[5:]
            input_steps.setdefault(step_id, v.strip())

        elif k.startswith('activity-'):
            activity_id = k[9:]
            input_activities.setdefault(activity_id, v.strip())

    blank_step_ids = form.get('blank_step_ids', '').split(',')
    blank_activity_ids = form.get('blank_activity_ids', '').split(',')

    depth = 1
    for step in learning.steps:
        if len(step.activities):
            depth = 2
            break

    return render_template('instruction_models/quiz.html',
                           instruction_model=instruction,
                           learning_model=learning,
                           blank_step_ids=blank_step_ids,
                           blank_activity_ids=blank_activity_ids,
                           input_steps=input_steps,
                           input_activities=input_activities,
                           depth=depth)
