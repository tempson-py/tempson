# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

class generatorTest(unittest.TestCase):

    def test_Empty_template(self):
        view = tempson.generator('<div>{{ a }}</div>')
        result = view.render({ 'a': 123 })
        try:
            self.assertEqual(result, '<div>123</div>')
        except AssertionError:
            coloredPrint('\n  [generator] × falied tokenize.', 'RED')
        else:
            coloredPrint('\n  [generator] √ successed tokenize.', 'GREEN')
        
