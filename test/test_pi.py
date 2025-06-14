import math
import os
import pytest
import yaml
from machin.formulae import load_formula
from webtools.tools import join

formulae_path = join(os.path.dirname(os.path.realpath(__file__)), "..", "formulae")


def q(n):
    if "/" in n:
        a, b = [int(i) for i in n.split("/")]
        return a / b
    return int(n)


@pytest.mark.parametrize(
    "file", sorted([file for file in os.listdir(formulae_path) if file.endswith(".pi")])
)
def test_is_pi(file):
    formula = load_formula(file[:-3])
    pi = sum(c * math.atan(1 / a) for c, a in formula.terms)
    assert abs(pi - math.pi) < 1e-10
