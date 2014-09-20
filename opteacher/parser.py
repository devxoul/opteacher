# -*- coding: utf-8 -*-

import os

from opteacher.ext import db
from opteacher.models.instruction_model import (
    InstructionModel,
    LearningModel,
    LearningStep,
    LearningActivity
)


_verbose = False


def parse_instruction_models(app):
    path = os.path.join(app.static_folder, 'data/instruction_models.txt')
    lines = open(path).readlines()
    subjects = {}
    subject = False

    for l in lines:
        line = l.decode('utf-8')

        # activity
        if line[:12] == ' ' * 12:
            instruction_model = subjects[subject]
            learning_model = instruction_model.learning_models[-1]
            step = learning_model.steps[-1]

            activity = LearningActivity()
            activity.learning_step = step
            activity.name = line.strip()
            db.session.add(activity)

        # step
        elif line[:8] == ' ' * 8:
            instruction_model = subjects[subject]
            learning_model = instruction_model.learning_models[-1]

            step = LearningStep()
            step.learning_model = learning_model
            step.name = line.strip()
            db.session.add(step)

        # learning model
        elif line[:4] == ' ' * 4:
            instruction_model = subjects[subject]

            learning_model = LearningModel()
            learning_model.instruction_model = instruction_model
            learning_model.name = line.strip()
            db.session.add(learning_model)

        # instruction model
        elif line[0] != ' ':
            instruction_model = InstructionModel()
            instruction_model.name = line.split(':')[1].strip()
            instruction_model.subject = line.split(':')[0].strip()
            subjects[subject] = instruction_model
            db.session.add(instruction_model)

    db.session.commit()

    if _verbose:
        for instruction_model in subjects.values():
            print instruction_model.name
            for learning_model in instruction_model.learning_models:
                print ' ' * 3, learning_model.name
                for step in learning_model.steps:
                    print ' ' * 7, step.name
                    for activity in step.activities:
                        print ' ' * 11, activity
