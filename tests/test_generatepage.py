from generatepage import extract_title
import unittest


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is a Title

and these are just some other words
and we will see
"""

        title = extract_title(md)
        self.assertEqual(title, "This is a Title")

    def test_extract_title_with_no_title(self):
        md = """
There is no title here
"""
        with self.assertRaises(Exception):
            _ = extract_title(md)
