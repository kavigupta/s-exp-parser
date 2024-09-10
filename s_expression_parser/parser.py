from typing import Union

import attr

from .lexer import PARENS, lex


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


@attr.s(eq=False, repr=False)
class Pair:
    car = attr.ib()
    cdr = attr.ib()

    def __eq__(self, other):
        comparisons_stack = [(self, other)]
        while comparisons_stack:
            a, b = comparisons_stack.pop()
            if isinstance(a, Pair) != isinstance(b, Pair):
                return False
            if not isinstance(a, Pair) and not isinstance(b, Pair):
                if a != b:
                    return False
                continue
            comparisons_stack.append((a.cdr, b.cdr))
            comparisons_stack.append((a.car, b.car))
        return True

    def __repr__(self):
        repr_each = {}
        attempted = set()
        stack = [self]
        while stack:
            current = stack.pop()
            if not isinstance(current, Pair):
                repr_each[id(current)] = repr(current)
                continue
            if id(current) in repr_each:
                continue
            if id(current.car) in repr_each and id(current.cdr) in repr_each:
                repr_car, repr_cdr = (
                    repr_each[id(current.car)],
                    repr_each[id(current.cdr)],
                )
                repr_each[id(current)] = f"Pair({repr_car}, {repr_cdr})"
                continue
            if id(current) in attempted:
                return "..."
            attempted.add(id(current))
            stack.append(current)
            stack.append(current.cdr)
            stack.append(current.car)
        return repr_each[id(self)]


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
            raise ValueError(f"Unmatched parenthesis {start}")
        if start in config.prefix_symbols:
            atom = parse_atom()
            return Pair(config.prefix_symbols[start], Pair(atom, nil))
        return start

    def parse_tail(close_paren):
        elements = []
        while token_stream and token_stream[-1] != close_paren:
            elements.append(parse_atom(close_paren))
        if not token_stream:
            raise ValueError("Unexpected end of file")
        assert token_stream.pop() == close_paren
        result: Union[Pair, nil] = nil
        for element in reversed(elements):
            if element == ".":
                # pylint: disable=no-member
                if result is nil or result.cdr is not nil:
                    raise ValueError(
                        "Invalid use of . in list; must be followed by a single atom, but was followed by "
                        + repr(result)
                    )
                result = result.car
            else:
                result = Pair(element, result)
        return result

    expressions = []
    while token_stream:
        expressions.append(parse_atom())
    return expressions
