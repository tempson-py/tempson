# -*- coding: utf-8 -*-

from tokenizer import *

LEFT_DELIMITERS  = '{{'
RIGHT_DELIMITERS = '}}'

class generator(object):

    def __init__(self, template, config = { "leftDelimiters": LEFT_DELIMITERS, "rightDelimiters": RIGHT_DELIMITERS }):
        self._config = config
        self.template = template

    def tokenizer(self):
        pass

    def render(self, variables):
        return self.template
