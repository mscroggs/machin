import math
import os
import pytest
from machin.formulae import load_formula
from webtools.tools import join

formulae_path = join(os.path.dirname(os.path.realpath(__file__)), "..", "formulae")
ids = sorted([file[:-3] for file in os.listdir(formulae_path) if file.endswith(".pi")])


@pytest.mark.parametrize("id", ids)
def test_is_pi(id):
    formula = load_formula(id)
    pi = sum(float(c) * math.atan(1 / float(a)) for c, a in formula.terms)
    assert abs(pi - math.pi) < 1e-10


@pytest.mark.parametrize("id", ids)
def test_terms_in_order(id):
    formula = load_formula(id)
    for (_, a), (_, b) in zip(formula.terms[:-1], formula.terms[1:]):
        assert a < b


def test_no_repeats():
    formulae = []
    duplicates = []
    for n, i in enumerate(ids):
        f0 = load_formula(i).compact_formula
        for i2, f1 in formulae:
            if f0 == f1:
                print(f"{i} and {i2} are equal")
                duplicates.append((i, i2))
        formulae.append((i, f0))
    assert len(duplicates) == 0


def test_no_gaps():
    for i, _ in enumerate(ids):
        assert "M" + f"000000{i}"[-6:] in ids


@pytest.mark.parametrize("id", ids)
def test_notes_full_stop(id):
    formula = load_formula(id)
    for note in formula._notes:
        assert note.endswith(".")


@pytest.mark.parametrize("id", ids)
def test_no_ones(id):
    formula = load_formula(id)
    for term in formula.terms:
        assert int(id[1:]) == 0 or term[1] != 1
