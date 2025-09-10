import math
import sympy  # type: ignore
import os
from arctans import Arctan, Zero, generate
from arctans.arctans import AbstractTerm
from machin.formulae import load_formula
from machin import settings

known_formulae = []

for file in os.listdir(settings.formulae_path):
    if file.endswith(".pi"):
        pi: AbstractTerm = Zero()
        for c, a in load_formula(file[:-3]).terms:
            pi += Arctan(c, 1 / sympy.S(a))
        known_formulae.append(pi)

for formula in known_formulae:
    assert (math.pi - float(formula)) < 0.0001

new_formulae = generate(known_formulae, max_terms=8, max_coefficient_denominator=1)
new_formulae = [formula for formula in new_formulae if 1 not in formula.term_dict]

pi_n = len(known_formulae)

for formula in new_formulae:
    with open(os.path.join("formulae", "M" + f"000000{pi_n}"[-6:] + ".pi"), "w") as f:
        for c, a in sorted(formula.terms, key=lambda ff: 1 / ff[1]):
            f.write(f"{c}[{1 / a}]\n")
    pi_n += 1
print(f"Found {len(new_formulae)} new formulae for pi")
