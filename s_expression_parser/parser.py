import attr

from .lexer import lex, PARENS


@attr.s
class ParserConfig:
    """
    Represents a parser configuration

    Arguments:
        prefix_symbols: Dictionary mapping individual characters to the special form
            they represent: e.g., {"'" : "quote", "`" : "quasiquote"}
        dots_are_cons: whether or not to alow expressions of the form (a . b)
    """

    prefix_symbols = attr.ib()
    dots_are_cons = attr.ib()

    def __attrs_post_init__(self):
        if "." in self.prefix_symbols and self.dots_are_cons:
            raise ValueError("Cannot use . both as a prefix symbol and cons")

    @property
    def symbols(self):
        return set(self.prefix_symbols) | ({"."} if self.dots_are_cons else set())


@attr.s
class Pair:
    car = attr.ib()
    cdr = attr.ib()


@attr.s
class nil:
    pass


nil = nil()


def parse(data, config):
    """
    Parses the given data using the given configuration.

    Arguments:
        data: the data string to be processed
        config: the configuration to use in parsing it
    Return:
        a list of Pair objects representing the s expressions provided
    """
    # reverse so pop works
    token_stream = lex(data, config.symbols)[::-1]

    def parse_atom(close_paren=None):
        if not token_stream:
            raise ValueError("Unexpected end of file")
        start = token_stream.pop()
        if start in PARENS:
            return parse_tail(PARENS[start])
        if start == close_paren:
            return None
        if start in PARENS.values():
            raise ValueError("Unmatched parenthesis {}".format(start))
        if start in config.prefix_symbols:
            atom = parse_atom()
            return Pair(config.prefix_symbols[start], Pair(atom, nil))
        return start

    def parse_tail(close_paren):
        first = parse_atom(close_paren)
        if first is None:
            return nil
        if first == "." and config.dots_are_cons:
            rest = parse_tail(close_paren)
            if not isinstance(rest, Pair) or rest.cdr != nil:
                raise ValueError(
                    (
                        "If dots are used to represent cons, then a dot"
                        " must be followed by a single atom, but instead was followed by {}"
                    ).format(rest)
                )
            return rest.car
        rest = parse_tail(close_paren)
        return Pair(first, rest)

    expressions = []
    while token_stream:
        expressions.append(parse_atom())
    return expressions
