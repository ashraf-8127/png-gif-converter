from pathlib import Path
files = sorted(
    Path(".").glob("*.png"),
    key=lambda x: int(x.stem)
)
for f in files:
    print(f.name)