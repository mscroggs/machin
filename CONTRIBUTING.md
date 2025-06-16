# Contributing to machin-like.org

## Making suggestions

If you want to report a mistake, suggest a new formula, or suggest any other improvement,
you can open an issue on the [GitHub issue tracker](https://github.com/mscroggs/machin/issues/new].

## Contributing directly

### Submitting a pull request
If you want to directly submit changes to machin-like.org, you can do this by forking the
[GitHub repository](https://github.com/mscroggs/machin),
making changes, then submitting a pull request.
If you want to contribute, but are unsure where to start, have a look at the
[issue tracker](https://github.com/mscroggs/machin/labels/good%20first%20issue) for issues labelled "good first issue".

### Defining an formula
Formulae on machin-like.org are defined using files in the `formulae/` folder with the `.pi` extension.
This file begins with metadata (im yaml format) between two lines containing only `--`, then has the terms of
the formula (in [compact notation](machin-like.md#Compact-notation)) on the following lines.
The entries in the metadata are:

<table class='bordered align-left'>
<thead>
<tr><td>Name</td><td>Required</td><td>Description</td></tr>
</thead>
<tr><td>`name`</td><td></td><td>The name of the formula (if it has a given name).</td></tr>
<tr><td>`alt&#8209;names`</td><td></td><td>Alternative names of the formula.</td></tr>
<tr><td>`notes`</td><td></td><td>Notes about the formula.</td></tr>
<tr><td>`references`</td><td></td><td>References to where the formula is defined.</td></tr>
</table>

### Testing your contribution
When you open a pull request, a series of tests and style checks will run via GitHub Actions.
(You may have to wait for manual approval for these to run.)
These tests and checks must pass before the pull request can be merged.
If the tests and checks fail, you can click on them on the pull request page to see where the failure is happening.

The style checks will check that the Python scripts that generate machin-like.org pass ruff checks.
If you've changed these scripts, you can run these checks locally by running:

```bash
python3 -m ruff format --check .
python3 -m ruff check .
```

Before you can run the tests or do a test build, you'll need to install the requirements:

```bash
python3 -m pip install -r requirements.txt
```

The tests can be run using:

```bash
python3 -m pytest test/
```

## Code of conduct
We expect all our contributors to follow our [code of conduct](CODE_OF_CONDUCT.md). Any unacceptable
behaviour can be reported to Matthew (machin@mscroggs.co.uk).
