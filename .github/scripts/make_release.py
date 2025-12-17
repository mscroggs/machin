import sys
from datetime import datetime

import github

_, tar_gz, version, access_key = sys.argv

git = github.Github(auth=github.Auth.Token(access_key))

machin = git.get_repo("mscroggs/machin")
branch = machin.get_branch("main")
ref = machin.get_git_ref("heads/main")

release = machin.create_git_tag_and_release(
    f"v{version}",
    f"v{version}",
    f"v{version}",
    f"Snapshot of machin-like.org, {datetime.now().strftime('%d %B %Y')}.\n\nThis release is archived on [Zenodo](https://zenodo.org/search?q=parent.id%3A17954248&f=allversions%3Atrue&sort=version).",
    branch.commit.sha,
    "commit",
)

for asset in release.get_assets():
    asset.delete_asset()

release.upload_asset(tar_gz)
