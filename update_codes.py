"""Update formulae files to have the correct number of digits in codes."""

import os
from machin import settings
from webtools.tools import join

for file in os.listdir(settings.formula_dir):
    if file.endswith(".pi"):
        if len(file) - 4 != settings.code_digits:
            assert len(file) - 4 < settings.code_digits
            new_file = file[0] + "0" * (settings.code_digits - len(file) + 4) + file[1:]
            os.system(f"mv {settings.formula_dir}/{file} {settings.formula_dir}/{new_file}")
