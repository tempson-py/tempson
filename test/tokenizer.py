# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

class compilerTest(unittest.TestCase):

    def test_template_type(self):
        with self.assertRaises(RuntimeError):
            token = tempson.compiler([])
            result = token.tokenize()
        coloredPrint('\n  [compiler] √ template type detect.', 'GREEN')

    def test_empty_template(self):
        token = tempson.compiler('')
        result = token.tokenize()
        self.assertEqual(result, [], 'Error tokenize empty template.')
        coloredPrint('\n  [compiler] √ empty template detect.', 'GREEN')

    def test_variable_template(self):
        token = tempson.compiler('<div>{{ a }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable template.')
        coloredPrint('\n  [compiler] √ variable template parse.', 'GREEN')

    def test_variable_with_expression_template(self):
        token = tempson.compiler('<div>{{ a + 1 }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a + 1 }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with expression template.')
        coloredPrint('\n  [compiler] √ expression template parse.', 'GREEN')

    def test_variable_with_string_expression_template(self):
        token = tempson.compiler('<div>{{ a + "}}" }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a + "}}" }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with string expression template.')
        coloredPrint('\n  [compiler] √ expression template parse (keywords contains).', 'GREEN')

    def test_block_template(self):
        token = tempson.compiler("""<div>
            {% for item in list %}
                {{ item }}
            {% endfor %}
        </div>""")
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>\n            '},
            {'type': 'BLKEXP', 'value': '{% for item in list %}'},
            {'type': 'HTML', 'value': '\n                '},
            {'type': 'VAREXP', 'value': '{{ item }}'},
            {'type': 'HTML', 'value': '\n            '},
            {'type': 'BLKEXP', 'value': '{% endfor %}'},
            {'type': 'HTML', 'value': '\n        </div>'}], 'Error tokenize variable with string expression template.')
        coloredPrint('\n  [compiler] √ block template parse.', 'GREEN')

    def test_comment_template(self):
        token = tempson.compiler("""<div>
            {* this is comments *}
            {* multi-line comments
               row1
               row2
             *}
        </div>""")
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>\n            '},
            {'type': 'COMEXP', 'value': '{* this is comments *}'},
            {'type': 'HTML', 'value': '\n            '},
            {'type': 'COMEXP', 'value': '{* multi-line comments\n               row1\n               row2\n             *}'},
            {'type': 'HTML', 'value': '\n        </div>'}], 'Error tokenize variable with string expression template.')
        coloredPrint('\n  [compiler] √ comments template parse.', 'GREEN')

    def test_raw_template(self):
        token = tempson.compiler("""<div>{{{ rawHTML }}}</div>""")
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'RAWEXP', 'value': '{{{ rawHTML }}}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with string expression template.')
        coloredPrint('\n  [compiler] √ raw template parse.', 'GREEN')
