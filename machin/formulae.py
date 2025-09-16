"""Machin-like formulae."""

import math
import os
import re
import typing
from warnings import warn

import yaml
from arctans import Integer, Rational
from arctans.numbers import RealNumber
from machin import settings
from webtools.markup import insert_links
from webtools.citations import make_bibtex, markup_citation
from webtools.tools import join


def load_value(n: str) -> RealNumber:
    if "/" in n:
        return Rational(*[int(i) for i in n.split("/")])
    return Integer(int(n))


class Formula:
    """A Machin-like formula."""

    def __init__(
        self,
        code: str,
        name: typing.Optional[str],
        alt_names: typing.List[str],
        terms: typing.List[typing.Tuple[RealNumber, RealNumber]],
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
        self._alt_names = alt_names
        self._references = []
        for r in references:
            id = None
            note = None
            if isinstance(r, str) and os.path.isfile(join(settings.references_path, r)):
                id = r
            if (
                isinstance(r, dict)
                and "id" in r
                and os.path.isfile(join(settings.references_path, r["id"]))
            ):
                id = r["id"]
                note = r.get("note")
            if id is not None:
                with open(join(settings.references_path, id)) as f:
                    ref = yaml.safe_load(f)
                    if note is not None:
                        ref["note"] = note
                    self._references.append(ref)
            else:
                self._references.append(r)

    @property
    def name(self) -> typing.Optional[str]:
        """Name."""
        return self._name

    @property
    def alt_names(self) -> typing.List[str]:
        """Alternative names."""
        return self._alt_names

    @property
    def html_name(self) -> str:
        """Html name."""
        if self.name is not None:
            return self.name
        return f"<code>{self.compact_formula}</code>"

    @property
    def text_name(self) -> str:
        """Text name."""
        if self.name is not None:
            return self.name
        return self.compact_formula

    @property
    def is_integer(self) -> bool:
        """Are all the arccotangents integers?"""
        for _, b in self.terms:
            if b.denominator != 1:
                return False
        return True

    @property
    def latex_formula(self) -> str:
        """Formula as LaTeX."""
        out = ""
        for coeff, arctan in self.terms:
            if coeff < 0:
                out += coeff.as_latex()
            else:
                if out != "":
                    out += "+"
                out += coeff.as_latex()
            out += f"\\arctan\\left({(1 / arctan).as_latex()}\\right)"
        return out

    @property
    def lehmer_measure(self) -> float | str:
        """Lehmer's measure."""
        for _, i in self.terms:
            if i == 1:
                return "INFINITY"
        return sum(1 / math.log10(float(i)) for _, i in self.terms)

    @property
    def compact_formula(self) -> str:
        out = ""
        for coeff, arctan in self.terms:
            if coeff < 0:
                if out != "":
                    out += " "
                out += f"- {-coeff}"
            else:
                if out != "":
                    out += " + "
                out += f"{coeff}"
            out += f"[{arctan}]"
        return out

    def notes(self, format: str = "HTML"):
        """Get notes."""
        match format:
            case "txt":
                return " ".join(self._notes)
            case "HTML":
                return "<br />".join([insert_links(i) for i in self._notes])
            case _:
                raise ValueError(f"Unsupported format: {format}")

    def references(self, format: str = "HTML"):
        """Get references."""
        match format:
            case "HTML":
                for r in self._references:
                    if isinstance(r, str):
                        warn(f"Incomplete reference: {r} (in {self.code})")
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
        content = f.read()
        if "--\n" in content:
            _, preamble, raw_terms = content.split("--\n")
            data = yaml.safe_load(preamble)
        else:
            data = {}
            raw_terms = content
    terms = [
        (load_value(term.split("[")[0]), load_value(term.split("[")[1][:-1]))
        for term in raw_terms.strip().split("\n")
    ]

    return Formula(
        code,
        data["name"] if "name" in data else None,
        data["alt-names"] if "alt-names" in data else [],
        terms,
        data["notes"] if "notes" in data else [],
        data["references"] if "references" in data else [],
    )
