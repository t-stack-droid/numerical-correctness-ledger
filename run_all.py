"""Run every script in repro/ and print a Markdown table of the outcomes.

With --log DIR, the full output of each script (exit status, stdout, stderr) is saved in DIR.
"""
import importlib.metadata as md
import pathlib
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
packages = ["scipy", "statsmodels", "networkx", "mne", "numpy", "mpmath"]
log_dir = pathlib.Path(sys.argv[sys.argv.index("--log") + 1]) if "--log" in sys.argv else None
if log_dir:
    log_dir.mkdir(parents=True, exist_ok=True)
versions = {}
for p in packages:
    try:
        versions[p] = md.version(p)
    except md.PackageNotFoundError:
        versions[p] = "not installed"
print("Versions: " + ", ".join(f"{k} {v}" for k, v in versions.items()))
print()
print("| Script | Outcome | Message |")
print("|---|---|---|")
for f in sorted((here / "repro").glob("*.py")):
    try:
        r = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        print(f"| {f.name} | timeout | no result within 600 s |")
        continue
    if log_dir:
        (log_dir / (f.stem + ".txt")).write_text(f"exit {r.returncode}\n--- stdout\n{r.stdout}\n--- stderr\n{r.stderr}")
    out = (r.stdout.strip().splitlines() or [""])[-1]
    if r.returncode == 1 and out.startswith("DEFECT PRESENT"):
        outcome = "present"
    elif r.returncode == 0:
        outcome = "not reproduced"
    else:
        outcome = "could not run"
        err = (r.stderr.strip().splitlines() or [""])[-1]
        out = err[:160]
    print(f"| {f.name} | {outcome} | {out.replace('|', '/')[:200]} |")
