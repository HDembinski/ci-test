from pathlib import PurePath as Path

project_dir = Path(__file__).parent.parent

with open(project_dir / "version.py") as f:
    version = {}
    exec(f.read(), version)
    version = version["version"]

print(version)
