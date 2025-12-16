import sys
from datetime import datetime

import github

version = datetime.now().strftime("%Y.%m")
version_branch = f"v{version}"

_, access_key = sys.argv

git = github.Github(auth=github.Auth.Token(access_key))

machin = git.get_repo("mscroggs/machin")
branch = machin.get_branch("main")
ref = machin.get_git_ref("heads/main")
base_tree = machin.get_git_tree(branch.commit.sha)

pyproject_file = machin.get_contents("pyproject.toml", branch.commit.sha)
pyproject = pyproject_file.decoded_content.decode("utf8")

pre_project, post_project = pyproject.split("[project]\n")
pre_version, post_version = post_project.split("version = ")
post_version = post_version.split("\n", 1)[1]

machin.create_git_ref(ref=f"refs/heads/{version_branch}", sha=branch.commit.sha)
new_branch = machin.get_branch(version_branch)
machin.update_file(
    "pyproject.toml",
    "[AUTOMATED] Update version number",
    f'{pre_project}[project]\n{pre_version}version = "{version}"\n{post_version}',
    sha=pyproject_file.sha,
    branch=version_branch,
)
pr = machin.create_pull(
    title="[AUTOMATED] Update version number", body="", base="main", head=version_branch
)
pr.enable_automerge("SQUASH")

print(f"branch={version_branch}")
