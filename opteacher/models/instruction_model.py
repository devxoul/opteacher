# -*- coding: utf-8 -*-


class InstructionModel(object):

    def __init__(self):
        self.name = None
        self.learning_models = []


class LearningModel(object):

    def __init__(self):
        self.subject = None
        self.name = None
        self.steps = []


class LearningStep(object):

    def __init__(self):
        self.name = None
        self.activities = []
