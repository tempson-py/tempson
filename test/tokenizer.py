import unittest
import tempson

defaultConfig = {
	"leftDelimiters":       '{{',
	"rightDelimiters":      '}}',
	"leftBlockDelimiters":  '{%',
	"rightBlockDelimiters": '%}'
}

class tokenizerTest(unittest.TestCase):

    def test_Empty_template(self):
        token = tempson.tokenizer('', defaultConfig)
        self.assertEqual(token.tokenGen(), [''], 'Error tokenize empty template.')

    def test_Variable_template(self):
        token = tempson.tokenizer('<div>{{a}}</div>', defaultConfig)
        self.assertEqual(token.tokenGen(), ['<div>', '{{a}}', '</div>'], 'Error tokenize variable template.')

    def test_Variable_with_space_template(self):
        token = tempson.tokenizer('<div>{{ a }}</div>', defaultConfig)
        self.assertEqual(token.tokenGen(), ['<div>', '{{ a }}', '</div>'], 'Error tokenize variable-with-space template.')

    def test_Variable_with_keywords_template(self):
        token = tempson.tokenizer('<div>\{{ a }}</div>', defaultConfig)
        self.assertEqual(token.tokenGen(), ['<div>', '\{{ a }}', '</div>'], 'Error tokenize variable-with-keywords template.')
