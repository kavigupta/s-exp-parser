import unittest

from timeout_decorator import timeout

from s_expression_parser import lex


class LexerTest(unittest.TestCase):
    @timeout(1)
    def test_basic_lex(self):
        self.assertEqual(lex("hi", {}), ["hi"])
        self.assertEqual(lex("123", {}), ["123"])
        self.assertEqual(lex('""', {}), ['""'])
        self.assertEqual(
            lex(r'"hi hi hi hi \n hi hi"', {}), [r'"hi hi hi hi \n hi hi"']
        )

    @timeout(1)
    def test_lex_with_comments(self):
        self.assertEqual(
            lex("hi; tahosetnuhasnetuhsnatehu thasntuht this doesn't matter", {}),
            ["hi"],
        )
        self.assertEqual(lex("hi;;;;;;; comment can have multiple things", {}), ["hi"])
        self.assertEqual(
            lex(
                "hi;;;;;;; comment can have multiple things\n but this is not a comment ; and this is",
                {},
            ),
            ["hi", "but", "this", "is", "not", "a", "comment"],
        )

    @timeout(1)
    def test_parens_lex(self):
        self.assertEqual(lex("()]", {}), ["(", ")", "]"])
        self.assertEqual(lex("(1 2 3)", {}), ["(", "1", "2", "3", ")"])
        self.assertEqual(lex("(1 223 3213)", {}), ["(", "1", "223", "3213", ")"])

    @timeout(1)
    def test_with_symbols(self):
        self.assertEqual(lex("abc", {}), ["abc"])
        self.assertEqual(lex("abc", {"a"}), ["a", "bc"])

    @timeout(1)
    def test_multiple_symbols(self):
        self.assertEqual(lex("abc", {"a", "ab"}), ["ab", "c"])
        self.assertEqual(lex("aaaaa", {"a", "aa"}), ["aa", "aa", "a"])
        self.assertEqual(lex("abc", {"b"}), ["a", "b", "c"])

    @timeout(1)
    def test_with_spaces_and_symbols(self):
        self.assertEqual(lex("a . b", {"."}), ["a", ".", "b"])
        self.assertEqual(lex('a . "a . b"', {"."}), ["a", ".", '"a . b"'])
