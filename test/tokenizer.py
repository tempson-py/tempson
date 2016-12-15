import unittest
import tempson

class complierTest(unittest.TestCase):

    def test_empty_template(self):
        token = tempson.complier('')
        result = token.tokenize()
        self.assertEqual(result, [], 'Error tokenize empty template.')

    def test_variable_template(self):
        token = tempson.complier('<div>{{ a }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable template.')

    def test_variable_with_expression_template(self):
        token = tempson.complier('<div>{{ a + 1 }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a + 1 }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with expression template.')

    def test_variable_with_string_expression_template(self):
        token = tempson.complier('<div>{{ a + "}}" }}</div>')
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'VAREXP', 'value': '{{ a + "}}" }}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with string expression template.')

    def test_block_template(self):
        token = tempson.complier("""<div>
            {% for item in list %}
                {{ item }}
            {% endfor %}
        </div>""")
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>\n            '},
            {'type': 'VAREXP', 'value': '{% for item in list %}'},
            {'type': 'HTML', 'value': '\n                '},
            {'type': 'VAREXP', 'value': '{{ item }}'},
            {'type': 'HTML', 'value': '\n            '},
            {'type': 'VAREXP', 'value': '{% endfor %}'},
            {'type': 'HTML', 'value': '\n        </div>'}], 'Error tokenize variable with string expression template.')

    def test_comment_template(self):
        token = tempson.complier("""<div>
            {* this is comments *}
            {* multi row comments
               row1
               row2
             *}
        </div>""")
        result = token.tokenize()
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>\n            '},
            {'type': 'COMEXP', 'value': '{* this is comments *}'},
            {'type': 'HTML', 'value': '\n            '},
            {'type': 'COMEXP', 'value': '{* multi row comments\n               row1\n               row2\n             *}'},
            {'type': 'HTML', 'value': '\n        </div>'}], 'Error tokenize variable with string expression template.')

    def test_raw_template(self):
        token = tempson.complier("""<div>{{{ rawHTML }}}</div>""")
        result = token.tokenize()
        print result
        self.assertEqual(result, [
            {'type': 'HTML', 'value': '<div>'},
            {'type': 'RAWEXP', 'value': '{{{ rawHTML }}}'},
            {'type': 'HTML', 'value': '</div>'}], 'Error tokenize variable with string expression template.')
