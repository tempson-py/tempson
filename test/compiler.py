# -*- coding: utf-8 -*-
import unittest
import tempson
from .coloredPrint import *

class compilerTest(unittest.TestCase):

    # TOKENIZER TEST #

    def test_template_type(self):
        try:
            with self.assertRaises(RuntimeError):
                token = tempson.compiler([])
                result = token.tokenize()
        except AssertionError:
            coloredPrint('\n  [tokenizer] × template type detect failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ template type detect.', 'GREEN')

    def test_empty_template(self):
        token = tempson.compiler('')
        result = token.tokenize()
        try:
            self.assertEqual(result, [])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × empty template detect failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ empty template detect.', 'GREEN')

    def test_variable_template(self):
        token = tempson.compiler('<div>{{ a }}</div>')
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>'},
                {'type': 'VAREXP', 'value': '{{ a }}'},
                {'type': 'HTML', 'value': '</div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × variable template parse failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ variable template parse.', 'GREEN')

    def test_variable_with_expression_template(self):
        token = tempson.compiler('<div>{{ a + 1 }}</div>')
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>'},
                {'type': 'VAREXP', 'value': '{{ a + 1 }}'},
                {'type': 'HTML', 'value': '</div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × error tokenize variable with expression template.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ expression template parse.', 'GREEN')

    def test_variable_with_string_expression_template(self):
        token = tempson.compiler('<div>{{ a + "}}" }}</div>')
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>'},
                {'type': 'VAREXP', 'value': '{{ a + "}}" }}'},
                {'type': 'HTML', 'value': '</div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × error tokenize variable with string expression template.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ expression template parse (keywords contains).', 'GREEN')

    def test_block_template(self):
        token = tempson.compiler("""<div>
            {% for item in list %}
                {{ item }}
            {% endfor %}
        </div>""")
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>\n            '},
                {'type': 'BLKEXP', 'value': '{% for item in list %}'},
                {'type': 'HTML', 'value': '\n                '},
                {'type': 'VAREXP', 'value': '{{ item }}'},
                {'type': 'HTML', 'value': '\n            '},
                {'type': 'BLKEXP', 'value': '{% endfor %}'},
                {'type': 'HTML', 'value': '\n        </div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × block template parse failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ block template parse.', 'GREEN')

    def test_comment_template(self):
        token = tempson.compiler("""<div>
            {* this is comments *}
            {* multi-line comments
               row1
               row2
             *}
        </div>""")
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>\n            '},
                {'type': 'COMEXP', 'value': '{* this is comments *}'},
                {'type': 'HTML', 'value': '\n            '},
                {'type': 'COMEXP', 'value': '{* multi-line comments\n               row1\n               row2\n             *}'},
                {'type': 'HTML', 'value': '\n        </div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × comments template parse failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ comments template parse.', 'GREEN')

    def test_raw_template(self):
        token = tempson.compiler("""<div>{{{ rawHTML }}}</div>""")
        result = token.tokenize()
        try:
            self.assertEqual(result, [
                {'type': 'HTML', 'value': '<div>'},
                {'type': 'RAWEXP', 'value': '{{{ rawHTML }}}'},
                {'type': 'HTML', 'value': '</div>'}
            ])
        except AssertionError:
            coloredPrint('\n  [tokenizer] × raw template parse failed.', 'RED')
        else:
            coloredPrint('\n  [tokenizer] √ raw template parse.', 'GREEN')

    # AST PARSER TEST #

    def test_ast_parser(self):
        doc = tempson.compiler("""<div>
            {% for item in list: %}
                {% if item == 1: %}
                    {{ item }}
                {% endif %}
                {% if item == 2: %}
                    {{ item }}
                {% endif %}
            {% endfor %}
        </div>""")
        tokens = doc.tokenize()
        result = doc.astParser(tokens)
        try:
            self.assertEqual(result, [{
                'type': 'HTML',
                'value': '<div>\n            '
            }, {
                'body': [{
                    'type': 'HTML',
                    'value': '\n                '
                }, {
                    'body': [{
                        'type': 'HTML',
                        'value': '\n                    '
                    }, {
                        'type': 'VAREXP',
                        'value': '{{ item }}'
                    }, {
                        'type': 'HTML',
                        'value': '\n                '
                    }],
                    'expression': 'item == 1',
                    'type': 'IFEXP'
                }, {
                    'type': 'HTML',
                    'value': '\n                '
                }, {
                    'body': [{
                        'type': 'HTML',
                        'value': '\n                    '
                    }, {
                        'type': 'VAREXP',
                        'value': '{{ item }}'
                    }, {
                        'type': 'HTML',
                        'value': '\n                '
                    }],
                    'expression': 'item == 2',
                    'type': 'IFEXP'
                }, {
                    'type': 'HTML',
                    'value': '\n            '
                }],
                'squence': 'list',
                'type': 'FOREXP',
                'iteratingVar': 'item'
            }, {
                'type': 'HTML',
                'value': '\n        </div>'
            }])
        except AssertionError:
            coloredPrint('\n  [ast parser] × ast parse failed.', 'RED')
        else:
            coloredPrint('\n  [ast parser] √ ast parse correct.', 'GREEN')
