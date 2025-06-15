"""Machin-like formulae."""

import math
import os
import re
import typing

import sympy  # type: ignore

import yaml
from machin import settings
from webtools.citations import make_bibtex, markup_citation
from webtools.tools import join


def load_value(n: str) -> sympy.core.expr.Expr:
    if "/" in n:
        return sympy.Rational(*[int(i) for i in n.split("/")])
    return sympy.Integer(n)


def as_latex(n: sympy.core.expr.Expr) -> str:
    if hasattr(n, "denominator"):
        if n.denominator == 1:
            return f"{n.numerator}"
        if isinstance(n, sympy.Rational):
            return f"\\frac{{{n.numerator}}}{{{n.denominator}}}"
    return f"{n}"


def as_compact(n: sympy.core.expr.Expr) -> str:
    if hasattr(n, "denominator"):
        if n.denominator == 1:
            return f"{n.numerator}"
        if isinstance(n, sympy.Rational):
            return f"{n.numerator}/{n.denominator}"
    return f"{n}"


class Formula:
    """A Machin-like formula."""

    def __init__(
        self,
        code: str,
        name: typing.Optional[str],
        terms: typing.List[typing.Tuple[sympy.core.expr.Expr, sympy.core.expr.Expr]],
        notes: typing.List[str],
        references: typing.List[typing.Dict[str, typing.Any] | str],
    ):
        """Create."""
        assert re.match(r"M[0-9]{6}", code)
        self.code = code
        self.index = int(code[1:])
        self.terms = terms
        self._notes = notes
        self._name = name
        self._references = []
        for r in references:
            if isinstance(r, str) and os.path.isfile(join(settings.references_path, r)):
                with open(join(settings.references_path, r)) as f:
                    self._references.append(yaml.safe_load(f))
            else:
                self._references.append(r)

    @property
    def name(self) -> typing.Optional[str]:
        """Name."""
        return self._name

    @property
    def html_name(self) -> str:
        """Html name."""
        if self.name is not None:
            return self.name
        return f"<code>{self.compact_formula}</code>"

    @property
    def latex_formula(self) -> str:
        """Formula as LaTeX."""
        out = ""
        for coeff, arctan in self.terms:
            if coeff < 0:
                out += as_latex(coeff)
            else:
                if out != "":
                    out += "+"
                out += as_latex(coeff)
            out += f"\\arctan\\left({as_latex(1 / arctan)}\\right)"
        return out

    @property
    def lehmer_measure(self) -> float:
        """Lehmer's measure."""
        return sum(1 / math.log10(float(i)) for _, i in self.terms)

    @property
    def compact_formula(self) -> str:
        out = ""
        for coeff, arctan in self.terms:
            if coeff < 0:
                if out != "":
                    out += " "
                out += "- " + as_compact(-coeff)
            else:
                if out != "":
                    out += " + "
                out += as_compact(coeff)
            out += f"[{as_compact(arctan)}]"
        return out

    def notes(self, format: str = "HTML"):
        """Get notes."""
        match format:
            case "txt":
                return " ".join(self._notes)
            case "HTML":
                return "<br />".join(self._notes)
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def references(self, format: str = "HTML"):
        """Get references."""
        match format:
            case "HTML":
                return "<br />".join(
                    f"<div class='citation'><code>{r}</code> (full reference coming soon)</div>"
                    if isinstance(r, str)
                    else f"<div class='citation'>{markup_citation(r, 'HTML')}</div>"
                    for r in self._references
                )
            case "txt":
                return " ".join(
                    f"[{r}]." if isinstance(r, str) else f"{markup_citation(r, 'txt')}."
                    for r in self._references
                )
            case "BibTeX":
                return "\n".join(
                    make_bibtex(f"{self.code}-{n + 1}", r) + "\n"
                    for n, r in enumerate(self._references)
                    if not isinstance(r, str)
                )
            case _:
                raise ValueError(f"Unsupported format: {format}")


def load_formula(code: str) -> Formula:
    """Load a formula from a file and folder."""
    with open(os.path.join(settings.formulae_path, f"{code}.pi")) as f:
        _, preamble, raw_terms = f.read().split("--\n")
    data = yaml.safe_load(preamble)
    terms = [
        (load_value(term.split("[")[0]), load_value(term.split("[")[1][:-1]))
        for term in raw_terms.strip().split("\n")
    ]

    return Formula(
        code,
        data["name"] if "name" in data else None,
        terms,
        data["notes"] if "notes" in data else [],
        data["references"] if "references" in data else [],
    )
