"""Build website."""

import argparse
import typing
import os
import re
from datetime import datetime

from machin import settings
from machin.formulae import load_formula
from webtools.html import make_html_page
from webtools.markup import heading, markup
from webtools.tools import html_local, join, parse_metadata

start_all = datetime.now()
path = os.path.dirname(os.path.realpath(__file__))
settings.set_root_path(join(path))
csv_first_line = "code,formula,name,Lehmer's measure,references,notes"
settings.settings.str_extras.append(("{{csv-first-line}}", csv_first_line))
settings.settings.str_extras.append(
    (
        "{{machin-count}}",
        str(
            sum(
                1 for file in os.listdir(settings.formulae_path) if file.endswith(".pi")
            )
        ),
    )
)

parser = argparse.ArgumentParser(description="Build website")
parser.add_argument(
    "destination",
    metavar="destination",
    nargs="?",
    default=None,
    help="Destination of HTML files.",
)
parser.add_argument(
    "--github-token",
    metavar="github_token",
    default=None,
    help="Provide a GitHub token to get update timestamps.",
)
parser.add_argument(
    "--local-prefix",
    metavar="local_prefix",
    default=None,
    help="Provide a GitHub token to get update timestamps.",
)

sitemap = {}


def write_html_page(
    path: str, title: str, content: str, include_in_sitemap: bool = True
):
    """Write a HTML page.

    Args:
        path: Page path
        title: Page title
        content: Page content
        include_in_sitemap: Should this page be included in the list of all pages?
    """
    global sitemap
    assert html_local(path) not in sitemap
    if include_in_sitemap:
        sitemap[html_local(path)] = title
    with open(path, "w") as f:
        f.write(make_html_page(content, title))


def load_md_file(matches):
    """Read the content of a markdown file."""
    with open(join(settings.root_path, matches[1])) as f:
        return f.read()


args = parser.parse_args()
if args.destination is not None:
    settings.set_html_path(args.destination)
if args.github_token is not None:
    settings.set_github_token(args.github_token)
if args.local_prefix is not None:
    settings.set_local_prefix(args.local_prefix)

# Prepare paths
if os.path.isdir(settings.html_path):
    os.system(f"rm -rf {settings.html_path}")
os.mkdir(settings.html_path)
os.mkdir(join(settings.html_path, "formulae"))

os.system(f"cp -r {settings.files_path}/* {settings.html_path}")

with open(os.path.join(settings.html_path, "CNAME"), "w") as f:
    f.write("machin-like.org")


def row(name, content):
    """Make a row of information."""
    if content == "":
        return ""
    else:
        return f"<tr><td>{name.replace(' ', '&nbsp;')}</td><td>{content}</td>"


formulae = []
formulae_for_index = []
formulae_for_integer_index = []
formulae_for_lehmer_index = []
formulae_for_min_b_index = []
formulae_for_max_b_index = []
formulae_for_nterms_indices: dict[int, list[tuple[str, str, str]]] = {}
formulae_by_year = {}
named_formulae_for_index = []
csv_rows = []

# Make formula pages
for file in os.listdir(settings.formulae_path):
    if file.endswith(".pi"):
        start = datetime.now()
        formula = file[:-3]
        print(f"{formula}.html", end="", flush=True)
        pi = load_formula(formula)
        rpath = join(settings.html_path, formula)
        os.mkdir(rpath)

        formulae_for_index.append((pi.code, pi.html_name, f"/{formula}"))
        if pi.is_integer:
            formulae_for_integer_index.append((pi.code, pi.html_name, f"/{formula}"))
        formulae_for_lehmer_index.append(
            (pi.lehmer_measure, pi.code, pi.html_name, f"/{formula}")
        )
        formulae_for_min_b_index.append((pi.terms[0][1], pi.html_name, f"/{formula}"))
        formulae_for_max_b_index.append((pi.terms[-1][1], pi.html_name, f"/{formula}"))
        if pi.name is not None:
            named_formulae_for_index.append((pi.code, pi.name, f"/{formula}"))
        formulae.append(pi)

        if len(pi.terms) not in formulae_for_nterms_indices:
            formulae_for_nterms_indices[len(pi.terms)] = []
        formulae_for_nterms_indices[len(pi.terms)].append(
            (pi.code, pi.html_name, f"/{formula}")
        )

        if pi.discovered_year is not None:
            if pi.discovered_year not in formulae_by_year:
                formulae_by_year[pi.discovered_year] = []
            formulae_by_year[pi.discovered_year].append((f"/{formula}", pi.html_name))

        if pi.name is None:
            content = heading("h1", f"{pi.code}")
        else:
            content = heading("h1", f"{pi.code}: {pi.name}")

        content += "<div style='overflow:scroll'>"
        content += f"$$\\pi={pi.latex_formula}$$"
        content += "</div>"

        content += "<table class='formula'>"
        if pi.name is not None:
            if len(pi.alt_names) == 0:
                content += row("Name", pi.name)
            else:
                content += row("Names", ", ".join([pi.name] + pi.alt_names))
        content += row("Compact formula", f"<code>{pi.compact_formula}</code>")
        content += row(
            "Lehmer's measure",
            "&infin;"
            if pi.lehmer_measure == "INFINITY"
            else f"{pi.lehmer_measure}"[:7],
        )
        content += row("Notes", pi.notes("HTML"))
        bib = pi.references("BibTeX")
        html = pi.references("HTML")
        if html != "":
            content += row(
                "References",
                html
                if bib == ""
                else (
                    f"{html}<br /><div class='citation'>"
                    f"<a href='/{pi.code}/references.bib'>Download references as BibTe&Chi;</a></div>"
                ),
            )
            with open(join(settings.html_path, pi.code, "references.bib"), "w") as f:
                f.write(bib)
        content += "</table>"

        csv_rows.append(
            ",".join(
                [
                    pi.code,
                    pi.compact_formula,
                    "" if pi.name is None else pi.name,
                    f"{pi.lehmer_measure}"[:7],
                    f'"{pi.references("txt")}"',
                    f'"{pi.notes("txt")}"',
                ]
            )
        )

        write_html_page(
            join(rpath, "index.html"), f"{formula}: {pi.text_name}", content
        )
        end = datetime.now()
        print(f" (completed in {(end - start).total_seconds():.2f}s)")

csv_rows.sort()
with open(join(settings.html_path, "formulae.csv"), "w") as f:
    f.write(f"{csv_first_line}\n")
    f.write("\n".join(csv_rows))


# Make pages
def make_pages(sub_dir=""):
    """Make pages recursively."""
    for file in os.listdir(join(settings.pages_path, sub_dir)):
        if os.path.isdir(join(settings.pages_path, sub_dir, file)):
            os.mkdir(join(settings.html_path, sub_dir, file))
            make_pages(join(sub_dir, file))
        elif file.endswith(".md"):
            start = datetime.now()
            fname = file[:-3]
            print(f"{sub_dir}/{fname}.html", end="", flush=True)
            with open(join(settings.pages_path, sub_dir, file)) as f:
                metadata, content = parse_metadata(f.read())

            content = content.replace(
                "{{ntermslinks}}",
                ", ".join(
                    f"[{n} term{'' if n == 1 else 's'}](/formulae/{n}-terms.html)"
                    for n in sorted(list(formulae_for_nterms_indices.keys()))
                ),
            )

            content = re.sub(r"\{\{(.+\.md)\}\}", load_md_file, content)
            content = content.replace("`--`", "`&#8209;&#8209;`")
            content = content.replace("](pages/", "](")
            content = markup(content, sub_dir)

            write_html_page(
                join(settings.html_path, sub_dir, f"{fname}.html"),
                metadata["title"],
                content,
            )
            end = datetime.now()
            print(f" (completed in {(end - start).total_seconds():.2f}s)")
        elif file.endswith(".html"):
            start = datetime.now()
            print(f"{sub_dir}/{file}", end="", flush=True)
            with open(join(settings.pages_path, sub_dir, file)) as f:
                metadata, content = parse_metadata(f.read())

            for a, b in settings.settings.re_extras:
                content = re.sub(a, b, content)
            for c, d in settings.settings.str_extras:
                content = content.replace(c, d)

            write_html_page(
                join(settings.html_path, sub_dir, file),
                metadata["title"],
                content,
            )
            end = datetime.now()
            print(f" (completed in {(end - start).total_seconds():.2f}s)")


make_pages()


def make_index_page(
    formulae: typing.List[typing.Tuple[str, str]],
    pagename: str,
    title: str,
    per_page: int = 50,
):
    content = heading("h1", title)
    if len(formulae) > per_page:
        content += (
            "<script type='text/javascript'>\n"
            "var cpage = 0;\n"
            "function change_page() {\n"
            "    document.getElementById('pagelist').innerHTML = '';\n"
            "    var ajax;\n"
            "    if(window.XMLHttpRequest){\n"
            "        ajax=new XMLHttpRequest();\n"
            "    } else {\n"
            "        ajax=new ActiveXObject('Microsoft.XMLHTTP');\n"
            "    }\n"
            "    ajax.onreadystatechange=function(){\n"
            "        if(ajax.readyState==4 && ajax.status==200){\n"
            "            document.getElementById('pagelist').innerHTML = ajax.responseText;\n"
            "        }\n"
            "    }\n"
        )
        if settings.local_prefix is None:
            content += f"    ajax.open('GET', '/formulae/{pagename}-' + cpage + '.html', true);\n"
        else:
            content += (
                f"    ajax.open('GET', '/{settings.local_prefix}/formulae/{pagename}-'"
                " + cpage + '.html', true);\n"
            )
        content += (
            "    ajax.send();\n"
            "}\n"
            "function next_page() {\n"
            "    cpage++;\n"
            "    change_page();\n"
            "}\n"
            "function prev_page() {\n"
            "    cpage--;\n"
            "    change_page();\n"
            "}\n"
            "</script>"
        )
    content += "<div id='pagelist'>"

    pages = []
    count = 0
    pcontent = ""
    last_title = ""
    for url, name in formulae:
        if url == "SECTION":
            if pcontent != "":
                pcontent += "</ul>"
            pcontent += heading("h2", name) + "<ul>"
            last_title = name
        else:
            if pcontent == "":
                pcontent += heading("h2", f"{last_title} (continued)")
                pcontent += "<ul>"
            pcontent += f"<li><a href='{url}'>{name}</a></li>"
            count += 1
            if count == per_page:
                pcontent += "</ul>"
                pages.append(pcontent)
                pcontent = ""
                count = 0
    if pcontent != "":
        pcontent += "</ul>"
        pages.append(pcontent)

    content += pages[0]
    if len(pages) > 0:
        content += (
            "<div class='nextlink'><a href='javascript:next_page()'>"
            f"Next {per_page} formulae &rarr;</a></div>"
        )

    for i, pcontent in enumerate(pages):
        with open(
            join(settings.html_path, "formulae", f"{pagename}-{i}.html"), "w"
        ) as f:
            if i > 0:
                f.write(
                    "<div class='nextlink'><a href='javascript:prev_page()'>"
                    f"&larr; Previous {per_page} formulae</a></div>"
                )
            f.write(pcontent)
            if i + 1 < len(pages):
                f.write(
                    "<div class='nextlink'><a href='javascript:next_page()'>"
                    f"Next {per_page} formulae &rarr;</a></div>"
                )

    write_html_page(
        join(settings.html_path, "formulae", f"{pagename}.html"), title, content
    )


# Alphabetical
named_formulae_for_index.sort(key=lambda i: i[1].lower())
make_index_page(
    [(url, f"{name} ({code})") for code, name, url in named_formulae_for_index],
    "alpha",
    "List of named Machin-like formulae (alphabetical)",
)

# Formulae by index
formulae_for_index.sort(key=lambda i: i[0])
make_index_page(
    [(url, f"{code}: {name}") for code, name, url in formulae_for_index],
    "index",
    "List of Machin-like formulae (by index)",
)

# By number of terms
for n in sorted(list(formulae_for_nterms_indices.keys())):
    formulae_for_nterms_indices[n].sort(key=lambda i: i[0].lower())
    make_index_page(
        [
            (url, f"{code}: {name}")
            for code, name, url in formulae_for_nterms_indices[n]
        ],
        f"{n}-terms",
        f"List of Machin-like formulae with {n} term{'' if n == 1 else 's'}",
    )

# Integer formulae by index
formulae_for_integer_index.sort(key=lambda i: i[0])
make_index_page(
    [(url, f"{code}: {name}") for code, name, url in formulae_for_integer_index],
    "integer",
    "List of Machin-like formulae with integer arccotangents (by index)",
)

# Formulae by Lehmer measure
largest_lehmer = max(
    i[0] for i in formulae_for_lehmer_index if not isinstance(i[0], str)
)
formulae_for_lehmer_index.sort(
    key=lambda i: largest_lehmer * 2 if i[0] == "INFINITY" else i[0]
)
make_index_page(
    [
        (url, f"{code}: {name} ({str(measure)[:7]})")
        for measure, code, name, url in formulae_for_lehmer_index
    ],
    "lehmer",
    "List of Machin-like formulae (by Lehmer's measure)",
)

# Formulae by smallest b
formulae_for_min_b_index.sort(key=lambda i: i[0])
make_index_page(
    [(url, name) for min_b, name, url in formulae_for_min_b_index],
    "min-b-smallest-first",
    "List of Machin-like formulae (by smallest arccotangent, low-to-high)",
)
make_index_page(
    [(url, name) for min_b, name, url in formulae_for_min_b_index[::-1]],
    "min-b-largest-first",
    "List of Machin-like formulae (by smallest arccotangent, high-to-low)",
)

# Formulae by largest b
formulae_for_max_b_index.sort(key=lambda i: i[0])
make_index_page(
    [(url, name) for max_b, name, url in formulae_for_max_b_index],
    "max-b-smallest-first",
    "List of Machin-like formulae (by largest arccotangent, low-to-high)",
)
make_index_page(
    [(url, name) for max_b, name, url in formulae_for_max_b_index[::-1]],
    "max-b-largest-first",
    "List of Machin-like formulae (by largest arccotangent, high-to-low)",
)

# Formulae by year
years = list(formulae_by_year.keys())
years.sort()
links = []
for y in years:
    links.append(("SECTION", f"{y}"))
    links += formulae_by_year[y]
make_index_page(
    links, "by-year", "List of Machin-like formulae by year discovered (oldest first)"
)
links = []
for y in years[::-1]:
    links.append(("SECTION", f"{y}"))
    links += formulae_by_year[y]
make_index_page(
    links,
    "by-year-reverse",
    "List of Machin-like formulae by year discovered (newest first)",
)

# Site map
sitemap[html_local(join(settings.html_path, "sitemap.html"))] = "List of all pages"


def list_pages(folder: str) -> str:
    """Create list of pages in a folder.

    Args:
        folder: The folder

    Returns:
        List of pages
    """
    items = []
    if folder == "":
        items.append(("A", "<li><a href='/index.html'>Front page</a>"))
    for i, j in sitemap.items():
        if i.startswith(folder):
            file = i[len(folder) + 1 :]
            if "/" in file:
                subfolder, subfile = file.split("/", 1)
                if subfile == "index.html":
                    items.append((j.lower(), list_pages(f"{folder}/{subfolder}")))
            elif file != "index.html":
                items.append((j.lower(), f"<li><a href='{i}'>{j}</a></li>"))
    items.sort(key=lambda a: a[0])
    out = ""
    if folder != "":
        title = sitemap[f"{folder}/index.html"]
        out += f"<li><a href='{folder}/index.html'>{title}</a>"
    out += "<ul>" + "\n".join(i[1] for i in items) + "</ul>"
    if folder != "":
        out += "</li>"
    return out


content = heading("h1", "List of all pages") + list_pages("")
with open(join(settings.html_path, "sitemap.html"), "w") as f:
    f.write(make_html_page(content))

end_all = datetime.now()
print(f"Total time: {(end_all - start_all).total_seconds():.2f}s")
