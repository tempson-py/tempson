# -*- coding: utf-8 -*-

from compiler import *

class generator(object):

    ast = None

    def __init__(self, template):
        self.template = template
        self.tokenizer()

    def tokenizer(self):
        token = compiler(self.template)
        self.ast = token.tokenize()

    def render(self, variables):
        return self.ast
