import unittest

from s_expression_parser import Pair, ParserConfig, nil, parse


class ParserTest(unittest.TestCase):
    def test_config_constructor(self):
        with self.assertRaises(ValueError):
            ParserConfig({".", "variadic"}, dots_are_cons=True)

    def test_parse_basic(self):
        self.assertEqual(
            parse("(+ 2 (3))", ParserConfig({}, False)),
            [Pair("+", Pair("2", Pair(Pair("3", nil), nil)))],
        )
        self.assertEqual(
            parse("(+ 2 [3])", ParserConfig({}, False)),
            [Pair("+", Pair("2", Pair(Pair("3", nil), nil)))],
        )
        self.assertEqual(
            parse("1 (2)", ParserConfig({}, False)),
            ["1", Pair("2", nil)],
        )

    def test_unmatched_parens(self):
        with self.assertRaises(ValueError):
            parse(")", ParserConfig({}, False))
        with self.assertRaises(ValueError):
            parse("(]", ParserConfig({}, False))
        with self.assertRaises(ValueError):
            parse("[)", ParserConfig({}, False))
        with self.assertRaises(ValueError):
            parse("(", ParserConfig({}, False))
        with self.assertRaises(ValueError):
            parse("(1 .)", ParserConfig({}, True))
        with self.assertRaises(ValueError):
            parse("(1 ')", ParserConfig({"'": "quote"}, True))

    def test_dots_are_cons(self):
        self.assertEqual(
            parse("(1 . 2)", ParserConfig({}, True)),
            [Pair("1", "2")],
        )
        self.assertEqual(
            parse("(1 . (2))", ParserConfig({}, True)),
            [Pair("1", Pair("2", nil))],
        )

    def test_prefixing(self):
        self.assertEqual(
            parse("('(1 2) hi)", ParserConfig({"'": "quote"}, False)),
            [
                Pair(
                    Pair("quote", Pair(Pair("1", Pair("2", nil)), nil)), Pair("hi", nil)
                )
            ],
        )

    def test_multi_char_prefix(self):
        self.assertEqual(
            parse("(,@(1 ,$) ,@hi)", ParserConfig({",@": "unquote-splicing"}, False)),
            [
                Pair(
                    Pair("unquote-splicing", Pair(Pair("1", Pair(",$", nil)), nil)),
                    Pair(Pair("unquote-splicing", Pair("hi", nil)), nil),
                )
            ],
        )

    def test_parse_extremely_long(self):
        count = 10**4
        structure = nil
        for _ in range(count):
            structure = Pair(nil, structure)
        self.assertEqual(
            parse("(" + "()" * count + ")", ParserConfig({}, False)),
            [structure],
        )
