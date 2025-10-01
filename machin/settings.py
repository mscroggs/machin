"""Settings."""

import os as _os
import yaml as _yaml

from webtools import settings
from webtools.tools import join as _join

root_path = ""
template_path = ""
files_path = ""
pages_path = ""
formulae_path = ""
html_path = ""
references_path = ""
data_path = ""
local_prefix: str | None = None

github_token: str | None = None

processes = 1

settings.owners = ["mscroggs"]
settings.url = "https://machin-like.org"
settings.website_name = [
    "Machin-like formulae",
    "Machin-like formulae",
]
settings.repo = "mscroggs/machin"

settings.github_token = github_token


def set_root_path(path: str):
    """Set root path."""
    global root_path
    global template_path
    global files_path
    global pages_path
    global formulae_path
    global html_path
    global references_path
    global data_path

    root_path = path
    template_path = _join(root_path, "template")
    files_path = _join(root_path, "files")
    pages_path = _join(root_path, "pages")
    formulae_path = _join(root_path, "formulae")
    references_path = _join(root_path, "references")
    data_path = _join(root_path, "data")

    settings.dir_path = root_path
    settings.template_path = template_path

    with open(_join(data_path, "contributors")) as f:
        settings.contributors = _yaml.load(f, Loader=_yaml.FullLoader)
    with open(_join(data_path, "editors")) as f:
        settings.editors = _yaml.load(f, Loader=_yaml.FullLoader)

    if html_path == "":
        html_path = _join(root_path, "_html")
        settings.html_path = html_path


def set_html_path(path: str):
    """Set HTML path."""
    global html_path
    html_path = path
    settings.html_path = path


def set_github_token(token: str):
    """Set GitHub token."""
    global github_token
    github_token = token
    settings.github_token = token


def set_local_prefix(prefix: str):
    """Set GitHub token."""
    global local_prefix
    local_prefix = prefix
    settings.local_prefix = prefix


if _os.path.isfile(
    _join(_os.path.dirname(_os.path.realpath(__file__)), "..", "README.md")
):
    set_root_path(_join(_os.path.dirname(_os.path.realpath(__file__)), ".."))

code_digits = 9
code_legacy_digits = [6]

settings.str_extras = [
    ("{{tick}}", "<span style='color:#008800'>&#10004;</span>"),
    ("{{code-digits}}", f"{code_digits}"),
]
