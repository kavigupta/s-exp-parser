from .parser import ParserConfig

cal_scheme = ParserConfig(
    {
        "'": "quote",
        "`": "quasiquote",
        ",": "unquote",
        ",@": "unquote-splicing",
        ".": "variadic",
    },
    dots_are_cons=False,
)

cal_scheme_with_dots = ParserConfig(
    {
        "'": "quote",
        "`": "quasiquote",
        ",": "unquote",
        ",@": "unquote-splicing",
    },
    dots_are_cons=True,
)
