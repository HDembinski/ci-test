from pathlib import PurePath as Path
import re
import subprocess as subp
from pkg_resources import parse_version

project_dir = Path(__file__).parent.parent

with open(project_dir / "version.py") as f:
    version = {}
    exec(f.read(), version)
    new_version = parse_version(version["version"])

latest_tag = next(
    iter(
        sorted(
            (
                parse_version(x)
                for x in subp.check_output(["git", "tag"]).decode().strip().split("\n")
            ),
            reverse=True,
        )
    )
)

# sanity checks
assert new_version > latest_tag

git_log = re.findall(
    r"[a-z0-9]+ ([^\n]+ \(#[0-9]+\))",
    subp.check_output(["git", "log", "--oneline", f"v{latest_tag}..HEAD"]).decode(),
)

print("\n".join(f"- {x}" for x in git_log))
