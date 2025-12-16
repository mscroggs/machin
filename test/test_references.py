import os
import pytest
import yaml
from machin import settings
from webtools.tools import join
from webtools.citations import template

ids = sorted(
    list(file for file in os.listdir(settings.references_path) if not file.startswith("."))
)


@pytest.mark.parametrize("id", ids)
def test_matches_template(id):
    with open(join(settings.references_path, id)) as f:
        ref = yaml.safe_load(f)

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

    assert all_in(ref, template)
