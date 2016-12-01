# -*- coding: utf-8 -*-

from tokenizer import *

defaultConfig = {
    "leftDelimiters":       '{{',
    "rightDelimiters":      '}}',
    "leftBlockDelimiters":  '{%',
    "rightBlockDelimiters": '%}'
}

class generator(object):

    def __init__(self, template, config = defaultConfig):
        self._config = config
        self.template = template

    def tokenizer(self):
        pass

    def render(self, variables):
        return self.template
