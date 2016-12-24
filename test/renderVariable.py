# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

renderer = tempson.renderer()

class renderVariableTest(unittest.TestCase):

    def test_wrong_ast(self):
        try:
            with self.assertRaises(RuntimeError):
                renderer.renderVariable({
                    'type': 'HTML',
                    'value': '<div>1</div>'
                }, {
                    'item': 1
                })
        except AssertionError:
            coloredPrint('\n  [renderer] × falied render wrong ast tree.', 'RED')
        else:
            coloredPrint('\n  [renderer] √ successed detect ast-dispatching wrong.', 'GREEN')

    def test_when_not_match_expressions(self):
        try:
            with self.assertRaises(RuntimeError):
                renderer.renderVariable({
                    'type': 'VAREXP',
                    'value': '{{ item'
                }, {
                    'item': 1
                })
        except AssertionError:
            coloredPrint('\n  [renderer] × falied detecting expression.', 'RED')
        else:
            coloredPrint('\n  [renderer] √ successed detect not-match-expressions.', 'GREEN')

    def test_render_variable(self):
        result = renderer.renderVariable({
            'type': 'VAREXP',
            'value': '{{ item }}'
        }, {
            'item': 1
        })
        try:
            self.assertEqual(result, '1')
        except AssertionError:
            coloredPrint('\n  [renderer] × falied render variable ast.', 'RED')
        else:
            coloredPrint('\n  [renderer] √ successed render variable ast.', 'GREEN')

    def test_render_expression(self):
        result = renderer.renderVariable({
            'type': 'VAREXP',
            'value': '{{ item + 1 }}'
        }, {
            'item': 1
        })
        try:
            self.assertEqual(result, '2')
        except AssertionError:
            coloredPrint('\n  [renderer] × falied render expression ast.', 'RED')
        else:
            coloredPrint('\n  [renderer] √ successed render expression ast.', 'GREEN')
        
