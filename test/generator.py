# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

class generatorTest(unittest.TestCase):

    def test_Empty_template(self):
        self.view = tempson.generator('<div>{{ a }}</div>')
        result = self.view.render({ 'a': 123 })
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>'},
                {'type': 'VAREXP', 'value': '{{ a }}'},
                {'type': 'HTML', 'value': '</div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [generator] × falied tokenize.', 'RED')
        else:
            coloredPrint('\n  [generator] √ successed tokenize.', 'GREEN')
        
