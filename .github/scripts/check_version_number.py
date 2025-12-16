import sys
import os

try:
    import tomllib
except ModuleNotFoundError:  # TODO: remove this once minimum Python version is 3.10
    import tomli as tomllib

import github

with open(
    os.path.join(
        os.path.join(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."),
            "..",
        ),
        "pyproject.toml",
    ),
    "rb",
) as f:
    version = tomllib.load(f)["project"]["version"]

_, access_key = sys.argv

git = github.Github(access_key)

machin = git.get_repo("mscroggs/machin")

for release in machin.get_releases():
    if release.tag_name == f"v{version}":
        print("release=no")
        break
else:
    print(f"release={version}")
