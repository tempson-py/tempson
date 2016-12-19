# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

vm = tempson.vm()

class vmTest(unittest.TestCase):

    def test_execute_code (self):
        result = vm.evalExpToStr('a + 3', { 'a': 1 }, True)
        try:
            self.assertEqual(result, '4', 'Evaluate error')
        except AssertionError:
            coloredPrint('\n  [sandbox] × falied evaluate expression to string.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ evaluate expression to string.', 'GREEN')

    def test_execute_code_with_import_expression (self):
        try:
            with self.assertRaises(RuntimeError):
                result = vm.evalExpToStr('import os', {}, True)
        except AssertionError:
            coloredPrint('\n  [sandbox] × sensitive word not detect.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ sensitive word detect.', 'GREEN')

    def test_execute_code_without_variable (self):
        try:
            with self.assertRaises(NameError):
                result = vm.evalExpToStr('a + 1', {}, True)
        except AssertionError:
            coloredPrint('\n  [sandbox] × evaluate expression failed (variable not defined).', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ evaluate expression (variable not defined).', 'GREEN')

    def test_execute_statement (self):
        try:
            with self.assertRaises(RuntimeError):
                result = vm.evalExpToStr('a = 1', {}, True)
        except AssertionError:
            coloredPrint('\n  [sandbox] × statement not detect.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ statement detect.', 'GREEN')

    def test_execute_code_without_xss_filter (self):
        result = vm.evalExpToStr('a + 3', { 'a': 1 }, False)
        try:
            self.assertEqual(result, '4', 'Turn off filter failed')
        except AssertionError:
            coloredPrint('\n  [sandbox] × ignore xss protect failed.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ ignore xss protect.', 'GREEN')

    def test_execute_code_context_with_xss (self):
        result = vm.evalExpToStr('a', { 'a': '<script>alert("123")</script>' }, True)
        try:
            self.assertEqual(result, '&lt;script&gt;alert("123")&lt;/script&gt;', 'Filter error')
        except AssertionError:
            coloredPrint('\n  [sandbox] × xss protect failed.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ xss protect.', 'GREEN')

    def test_evaluate_boolean_value (self):
        result = vm.evalExpToBool('a == b', {
            'a': 1,
            'b': 1})
        try:
            self.assertEqual(result, True, 'Evaluate error')
        except AssertionError:
            coloredPrint('\n  [sandbox] × evaluate expression to boolean failed.', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ evaluate expression to boolean.', 'GREEN')

    def test_evaluate_boolean_value_false (self):
        result = vm.evalExpToBool('a is not b', {
            'a': 1,
            'b': 1})
        try:
            self.assertEqual(result, False, 'Evaluate error')
        except AssertionError:
            coloredPrint('\n  [sandbox] × evaluate expression to boolean failed (python syntax).', 'RED')
        else:
            coloredPrint('\n  [sandbox] √ evaluate expression to boolean (python syntax).', 'GREEN')
