"""Machin-like formulae."""

import math
import os
import re
import typing

import sympy

import yaml
from machin import settings
from webtools.citations import make_bibtex, markup_citation
from webtools.tools import html_local


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
        references: typing.List[typing.Dict[str, typing.Any]],
    ):
        """Create."""
        assert re.match(r"M[0-9]{6}", code)
        self.code = code
        self.index = int(code[1:])
        self._terms = terms
        self._notes = notes
        self._name = name
        self._references = references

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
        for coeff, arctan in self._terms:
            if coeff < 0:
                out += as_latex(coeff)
            else:
                if out != "":
                    out += "+"
                out += as_latex(coeff)
            out += f"\\arctan\\left({as_latex(1/arctan)}\\right)"
        return out

    @property
    def lehmer_measure(self) -> float:
        """Lehmer's measure."""
        return sum(1/math.log10(float(i)) for _, i in self._terms)

    @property
    def compact_formula(self) -> str:
        out = ""
        for coeff, arctan in self._terms:
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
            case "HTML":
                return "<br />".join(self._notes)
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def references(self, format: str = "HTML"):
        """Get references."""
        match format:
            case "HTML":
                return "<br />".join(
                    f"<div class='citation'>{to_html(markup_citation(r))}</div>"
                    for r in self._references
                )
            case "BibTeX":
                return "\n".join(
                    make_bibtex(f"{self.code}-{n + 1}", r) + "\n"
                    for n, r in enumerate(self._references)
                )
            case _:
                raise ValueError(f"Unsupported format: {format}")


def load_formula(code: str) -> Formula:
    """Load a formula from a file and folder."""
    with open(os.path.join(settings.formulae_path, f"{code}.pi")) as f:
        _, preamble, terms = f.read().split("--\n")
    data = yaml.safe_load(preamble)
    terms = [
        (load_value(term.split("[")[0]), load_value(term.split("[")[1][:-1]))
        for term in terms.strip().split("\n")
    ]

    return Formula(
        code,
        data["name"] if "name" in data else None,
        terms,
        data["notes"] if "notes" in data else [],
        data["references"] if "references" in data else [],
    )
