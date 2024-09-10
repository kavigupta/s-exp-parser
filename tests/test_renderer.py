import unittest
from textwrap import dedent

from s_expression_parser import Pair, ParserConfig, Renderer, nil, parse


def process(string):
    return dedent(string).strip()


class ParserTest(unittest.TestCase):
    @staticmethod
    def parse_and_rerender(string, **kwargs):
        return Renderer(**kwargs).render_multiple(
            parse(string, ParserConfig({"'", "quote"}, True))
        )

    def test_render_basic(self):
        self.assertEqual(
            Renderer().render("1"),
            process(
                """
                1
                """
            ),
        )
        self.assertEqual(
            Renderer().render(Pair("1", nil)),
            process(
                """
                (1)
                """
            ),
        )
        self.assertEqual(
            Renderer().render(Pair("1", "2")),
            process(
                """
                (1 . 2)
                """
            ),
        )
        self.assertEqual(
            Renderer().render(Pair("1", Pair("2", Pair("3", nil)))),
            process(
                """
                (1 2 3)
                """
            ),
        )
        self.assertEqual(
            self.parse_and_rerender("(1 2 (3 (4)))"),
            process(
                """
                (1 2 (3 (4)))
                """
            ),
        )
        self.assertEqual(
            self.parse_and_rerender("(1 2 (3 (4 ())))"),
            process(
                """
                (1 2 (3 (4 ())))
                """
            ),
        )

    def test_wrapping(self):
        self.assertEqual(
            self.parse_and_rerender("(1 2 3 4 5 6 (7) (8))", columns=10),
            process(
                """
                (1
                  2
                  3
                  4
                  5
                  6
                  (7)
                  (8)
                )
                """
            ),
        )
        self.assertEqual(
            self.parse_and_rerender(
                """
                (define (factorial x)
                    (if (zero? x)
                        1
                        (* x (factorial (- x 1)))))
                """,
                columns=40,
            ),
            process(
                """
                (define
                  (factorial x)
                  (if
                    (zero? x)
                    1
                    (* x (factorial (- x 1)))
                  )
                )
                """
            ),
        )

    def test_nil_as_word(self):
        self.assertEqual(
            Renderer(nil_as_word=True).render(nil),
            process(
                """
                nil
                """
            ),
        )

        self.assertEqual(
            Renderer(nil_as_word=True, columns=10).render_multiple(
                parse("(1 2 3 4 5 6 (7) (8) ())", ParserConfig({"'", "quote"}, True))
            ),
            process(
                """
                (1
                  2
                  3
                  4
                  5
                  6
                  (7)
                  (8)
                  nil
                )
                """
            ),
        )

    def test_nil_as_word_in_list(self):
        self.assertEqual(
            Renderer(nil_as_word=True, columns=10).render(Pair(nil, nil)),
            process(
                """
                (nil)
                """
            ),
        )

    def test_nil_as_word_large(self):
        text = Renderer(nil_as_word=True, columns=10).render_multiple(
            parse(
                "(Module (FunctionDef &f:0 (arguments () ((arg &x:1 None None)) None () () None ()) (semi (FunctionDef &g:1 (arguments () ((arg &x:2 None None)) None () () None ((Name &x:1 (Load)))) (Return (Name &x:2 (Load))) () None None) (Return (Name &x:1 (Load)))) () None None) ())",
                ParserConfig({"'", "quote"}, True),
            ),
        )
        self.assertFalse("()" in text)

    def test_render_extremely_long(self):
        count = 10**4
        structure = nil
        for _ in range(count):
            structure = Pair(nil, structure)
        # print(structure)
        self.assertEqual(
            "(\n" + "  ()\n" * count + ")",
            Renderer(columns=1).render(structure),
        )
