import unittest
import tempson

class generatorTest(unittest.TestCase):

    def test_Empty_template(self):
        self.template = tempson.generator("<div>{{ a }}</div>")
        self.assertEqual(self.template.render({ "a": 123 }), '<div>{{ a }}</div>')
