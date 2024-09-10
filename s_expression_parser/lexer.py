PARENS = {"(": ")", "[": "]"}


def lex(data, special_symbols):
    """
    Lexes the given string, as 61a-scheme compatible scheme code. This handles
        numbers, parentheses, and the given special symbols.

    Arguments
        data: the data to parse
        special_symbols: the set of symbols to handle
    """
    special_symbols = (
        set(special_symbols) | set(PARENS.keys()) | set(PARENS.values()) | {";"}
    )

    special_symbols = sorted(special_symbols, key=lambda x: (-len(x), x))

    symbol_stream = list(data)[::-1]  # reverse to pop from the front
    tokens = []

    def lex_single_token():
        current = symbol_stream[-1]
        if current.isspace():
            symbol_stream.pop()
            return
        if current == ";":
            while symbol_stream and symbol_stream[-1] != "\n":
                symbol_stream.pop()
            return
        for symbol in special_symbols:
            last_idx = -len(symbol)
            if symbol_stream[last_idx:] == list(symbol)[::-1]:
                symbol_stream[last_idx:] = []
                tokens.append(symbol)
                return
        if current == '"':
            token_items = [symbol_stream.pop()]
            while symbol_stream:
                current = symbol_stream[-1]
                token_items.append(symbol_stream.pop())
                if current == '"':
                    break
                if current == "\\":
                    if not symbol_stream:
                        raise SyntaxError("unexpected EOF when parsing string")
                    token_items.append(symbol_stream.pop())
            tokens.append("".join(token_items))
            return
        token_items = [symbol_stream.pop()]
        while symbol_stream:
            current = symbol_stream[-1]
            if current.isspace() or current in special_symbols:
                break
            token_items.append(symbol_stream.pop())
        tokens.append("".join(token_items))
        return

    while symbol_stream:
        lex_single_token()

    return tokens
