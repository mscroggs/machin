import math
import os
import pytest
import yaml
from webtools.tools import join

formulae_path = join(os.path.dirname(os.path.realpath(__file__)), "..", "formulae")


def q(n):
    if "/" in n:
        a, b = [int(i) for i in n.split("/")]
        return a / b
    return int(n)


@pytest.mark.parametrize("file", [
    file for file in os.listdir(formulae_path) if file.endswith(".pi")
])
def test_is_pi(file):
    with open(join(formulae_path, file)) as f:
        _, data, terms = f.read().split("--\n")
    data = yaml.safe_load(data)
    terms = terms.strip().split("\n")
    pi = 0
    for term in terms:
        if term[0] == "[":
            c = 1
        else:
            c = q(term.split("[")[0])
        a = q(term.split("[")[1].split("]")[0])
        pi += c * math.atan(1/a)
    assert abs(pi - math.pi) < 1e-10
