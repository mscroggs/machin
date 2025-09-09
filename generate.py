import math
import sympy
import os
from arctans import Arctan, Zero, generate
from machin.formulae import load_formula
from machin import settings

known_formulae = []

for file in os.listdir(settings.formulae_path):
    if file.endswith(".pi"):
        pi = Zero()
        for c, a in load_formula(file[:-3]).terms:
            pi += Arctan(c, 1 / sympy.S(a))
        known_formulae.append(pi)

for f in known_formulae:
    assert (math.pi - float(f)) < 0.0001

new_formulae = [
    f for f in generate(known_formulae, max_terms=8)
    if 1 not in f.term_dict
]

pi_n = len(known_formulae) + 1

for formula in new_formulae:
    with open("M" + f"000000{pi_n}"[-6:] + ".pi", "w") as f:
        for c, a in formula.terms:
            f.write(f"{c}[{1/a}]\n")
    pi_n += 1
print(f"Found {len(new_formulae)} new formulae for pi")
