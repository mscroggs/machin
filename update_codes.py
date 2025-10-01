"""Update formulae files to have the correct number of digits in codes."""

import os
from machin import settings

for file in os.listdir(settings.formulae_path):
    if file.endswith(".pi"):
        if len(file) - 4 != settings.code_digits:
            assert len(file) - 4 < settings.code_digits
            new_file = file[0] + "0" * (settings.code_digits - len(file) + 4) + file[1:]
            print(f"renaming {file} to {new_file}")
            os.system(
                f"mv {settings.formulae_path}/{file} {settings.formulae_path}/{new_file}"
            )
