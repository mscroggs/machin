import math
import os
import pytest
import yaml
from machin import settings
from machin.formulae import load_formula
from webtools.tools import join
import webtools


def insert_webtools_template(d):
    out = {}
    for i, j in d.items():
        if isinstance(j, dict):
            out[i] = insert_webtools_template(j)
        elif j == "webtools.citations.template":
            out[i] = webtools.citations.template
            out[i]["id"] = None
        else:
            out[i] = j
    return out


ids = sorted([file[:-3] for file in os.listdir(settings.formulae_path) if file.endswith(".pi")])
with open(join(settings.root_path, "template.pi")) as f:
    template = insert_webtools_template(yaml.safe_load(f))


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
        assert "M" + ("0" * settings.code_digits + f"{i}")[-settings.code_digits :] in ids


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


@pytest.mark.parametrize("id", ids)
def test_metadata(id):
    with open(join(settings.formulae_path, f"{id}.pi")) as f:
        content = f.read().split("--")
    assert len(content) in [1, 3]
    if len(content) == 1:
        return
    metadata = content[1]
    data = yaml.safe_load(metadata)

    def all_in(a, b):
        assert isinstance(b, dict)
        for i in a:
            if i not in b:
                return False
            if isinstance(a[i], dict):
                if not all_in(a[i], b[i]):
                    return False
            elif isinstance(a[i], list):
                for j in a[i]:
                    if isinstance(j, dict) and not all_in(j, b[i]):
                        return False
            else:
                assert isinstance(a[i], (str, int))
        for i, j in b.items():
            if j == "REQUIRED" and i not in a:
                if set(a.keys()) != {"id", "note"}:
                    return False
        return True

    assert all_in(data, template)
