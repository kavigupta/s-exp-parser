import unittest
from timeout_decorator import timeout
from textwrap import dedent

from s_expression_parser import parse, ParserConfig, Pair, nil, Renderer


def process(string):
    return dedent(string).strip()


class ParserTest(unittest.TestCase):
    def parse_and_rerender(self, string, **kwargs):
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
