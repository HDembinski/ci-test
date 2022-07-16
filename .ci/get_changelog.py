from pathlib import PurePath as Path
import re
import subprocess as subp
from pkg_resources import parse_version
import sys

new_version = None
latest_tag = None

if len(sys.argv) > 1:
    latest_tag = sys.argv[1]
    latest_tag = parse_version(latest_tag)
    if len(sys.argv) == 3:
        new_version = sys.argv[2]
        new_version = parse_version(new_version)

project_dir = Path(__file__).parent.parent

if new_version is None:
    with open(project_dir / "version.py") as f:
        version = {}
        exec(f.read(), version)
        new_version = parse_version(version["version"])

if latest_tag is None:
    latest_tag = next(
        iter(
            sorted(
                (
                    parse_version(x)
                    for x in subp.check_output(["git", "tag"])
                    .decode()
                    .strip()
                    .split("\n")
                ),
                reverse=True,
            )
        )
    )

# sanity checks
assert new_version > latest_tag, f"{new_version} > {latest_tag}"

git_log = re.findall(
    r"[a-z0-9]+ ([^\n]+ \(#[0-9]+\))",
    subp.check_output(["git", "log", "--oneline", f"v{latest_tag}..HEAD"]).decode(),
)

print("## What's Changed\n")
if git_log:
    print("".join(f"- {x}\n" for x in git_log))
else:
    print("- Various minor improvements\n")
print(
    f"**Full Changelog**: https://github.com/scikit-hep/pyhepmc/compare/v{latest_tag}...v{new_version}"
)
