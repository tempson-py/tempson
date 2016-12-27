# -*- coding: utf-8 -*-

from compiler import *
from renderer import *

r = renderer()

class generator(object):

    ast = None

    def __init__(self, template):
        self.template = template
        self.tokenizer()

    def tokenizer(self):
        com = compiler(self.template)
        tokens = com.tokenize()
        self.ast = com.astParser(tokens)

    def render(self, scope):
        html = ''

        for ast in self.ast:
            if ast['type'] == 'HTML':
                html += ast['value']
            elif ast['type'] == 'VAREXP':
                renderResult = r.renderVariable(ast, scope)
                if isinstance(renderResult, str):
                    html += renderResult
                else:
                    raise RuntimeError('Unknown renderer error in render variable-expression')
            elif ast['type'] == 'RAWEXP':
                renderResult = r.renderVariable(ast, scope, True)
                if isinstance(renderResult, str):
                    html += renderResult
                else:
                    raise RuntimeError('Unknown renderer error in render rawHTML-expression')
            elif ast['type'] == 'IFEXP':
                renderResult = r.renderIfExpression(ast, scope)
                if isinstance(renderResult, str):
                    html += renderResult
                else:
                    raise RuntimeError('Unknown renderer error in render if-expression')
            elif ast['type'] == 'FOREXP':
                renderResult = r.renderForExpression(ast, scope)
                if isinstance(renderResult, str):
                    html += renderResult
                else:
                    raise RuntimeError('Unknown renderer error in render for-expression')

        return html
