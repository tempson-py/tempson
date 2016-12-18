import unittest
import tempson

vm = tempson.vm()

class vmTest(unittest.TestCase):

    def test_execute_code (self):
        result = vm.evalExpToStr('''a + 3''', { 'a': 1 }, True)
        self.assertEqual(result, '4', 'Evaluate error')

    def test_execute_code_with_import_expression (self):
        with self.assertRaises(RuntimeError):
            result = vm.evalExpToStr('''import os''', {}, True)

    def test_execute_code_without_xss_filter (self):
        result = vm.evalExpToStr('''a + 3''', { 'a': 1 }, False)
        self.assertEqual(result, '4', 'Turn off filter failed')

    def test_execute_code_context_with_xss (self):
        result = vm.evalExpToStr('''a''', { 'a': '<script>alert("123")</script>' }, True)
        self.assertEqual(result, '&lt;script&gt;alert("123")&lt;/script&gt;', 'Filter error')
