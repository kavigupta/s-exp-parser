import attr

from .parser import Pair, nil


@attr.s
class Renderer:
    indent = attr.ib(default=2)
    columns = attr.ib(default=120)
    nil_as_word = attr.ib(default=False)

    def render_multiple(self, parsed):
        return "".join(self.render(x) for x in parsed)

    def render(self, parsed):
        return self._render(self._to_list(parsed))

    def _render(self, parsed, indent=0):
        if isinstance(parsed, str):
            return self._indent(parsed, indent)

        if not parsed:
            return self._indent("nil" if self.nil_as_word else "()", indent)

        single_line = self._indent(self._render_one_line(parsed), indent)
        if len(single_line) <= self.columns:
            return single_line

        assert isinstance(parsed, list)
        parsed = parsed[:]
        start = self._indent("(", indent)
        if isinstance(parsed[0], str):
            start += parsed.pop(0)
        return "\n".join(
            [start]
            + [self._render(x, indent + 1) for x in parsed]
            + [self._indent(")", indent)]
        )

    def _render_one_line(self, parsed):
        if isinstance(parsed, str):
            return parsed
        if not parsed:
            return "nil" if self.nil_as_word else "()"
        return "(" + " ".join(self._render_one_line(x) for x in parsed) + ")"

    def _indent(self, string, indentation):
        assert "\n" not in string
        return " " * indentation * self.indent + string

    def _to_list(self, parsed):
        if parsed is nil:
            return []
        if not isinstance(parsed, Pair):
            return parsed
        stack = [([], parsed)]
        while True:
            current_list, current_pair = stack.pop()
            if current_pair is nil:
                if not stack:
                    return current_list
                stack[-1][0].append(current_list)
                continue
            if not isinstance(current_pair, Pair):
                if current_list:
                    current_list.append(".")
                    current_list.append(current_pair)
                else:
                    current_list = current_pair
                if not stack:
                    return current_list
                stack[-1][0].append(current_list)
                continue
            stack.append((current_list, current_pair.cdr))
            stack.append(([], current_pair.car))
