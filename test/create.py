# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

class finalTest(unittest.TestCase):

    def test_createFragment(self):
        fragment = tempson.createFragment('<div>{{ a }}</div>')
        result = fragment.render({ 'a': 123 })
        try:
            self.assertEqual(result, '<div>123</div>')
        except AssertionError:
            coloredPrint('\n  [createFragment] × falied create from fragment.', 'RED')
        else:
            coloredPrint('\n  [createFragment] √ successed create from fragment.', 'GREEN')

    def test_createDoc(self):
        fragment = tempson.createDoc('./test/index.tpl')
        result = fragment.render({
            'list': [{
                'name': 'Jason',
                'age': 20
            }, {
                'name': 'Alice',
                'age': 21
            }]
        })
        print result
        try:
            self.assertEqual(result, '<div>123</div>')
        except AssertionError:
            coloredPrint('\n  [createFragment] × falied create from fragment.', 'RED')
        else:
            coloredPrint('\n  [createFragment] √ successed create from fragment.', 'GREEN')
