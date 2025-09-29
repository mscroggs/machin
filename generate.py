import math
import os
from datetime import datetime
from arctans import arctan, arccotan, generate, one
from machin.formulae import load_formula
from machin import settings

known_formulae = []

for file in os.listdir(settings.formulae_path):
    if file.endswith(".pi"):
        pi = arctan(0)
        for c, a in load_formula(file[:-3]).terms:
            pi += c * arccotan(a)
        known_formulae.append(pi)

for formula in known_formulae:
    assert (math.pi - float(formula)) < 0.0001

new_formulae = generate(
    known_formulae, max_terms=8, max_coefficient_denominator=1, printing=True
)
new_formulae = [formula for formula in new_formulae if one not in formula.term_dict]

pi_n = len(known_formulae)

now = datetime.now()

for formula in new_formulae:
    with open(os.path.join("formulae", "M" + f"000000{pi_n}"[-6:] + ".pi"), "w") as f:
        f.write("--\n")
        f.write(f"day: {now.day}\n")
        f.write(f"month: {now.month}\n")
        f.write(f"day: {now.year}\n")
        f.write("--\n")
        for coeff, arct in sorted(formula.terms, key=lambda ff: 1 / ff[1]):
            f.write(f"{coeff}[{1 / arct}]\n")
    pi_n += 1
print(f"Found {len(new_formulae)} new formulae for pi")
