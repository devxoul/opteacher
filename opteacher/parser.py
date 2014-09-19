# -*- coding: utf-8 -*-

from flask import g

from models.instruction_model import InstructionModel, LearningModel,\
    LearningStep

import os


def parse_instruction_models(app):
    path = os.path.join(app.static_folder, 'data/instruction_models.txt')
    lines = open(path).readlines()
    subjects = {}
    subject = False

    for l in lines:
        line = l.decode('utf-8')
        if line[0] != ' ':
            instruction = InstructionModel()
            instruction.name = line.split(':')[1].strip()
            subject = line.split(':')[0].strip()
            subjects[subject] = instruction

        elif line[:12] == ' ' * 12:
            step = subjects[subject].learning_models[-1].steps[-1]
            step.activities.append(line.strip())

        elif line[:8] == ' ' * 8:
            step = LearningStep()
            step.name = line.strip()
            subjects[subject].learning_models[-1].steps.append(step)

        elif line[:4] == ' ' * 4:
            model = LearningModel()
            model.name = line.strip()
            model.subject = subject
            subjects[subject].learning_models.append(model)

    for instruction_model in subjects.values():
        print instruction_model.name
        for learning_model in instruction_model.learning_models:
            print ' ' * 3, learning_model.name
            for step in learning_model.steps:
                print ' ' * 7, step.name
                for activity in step.activities:
                    print ' ' * 11, activity
    g.instruction_models = subjects
