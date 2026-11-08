"""Run the tool on NEW input, no chat needed.

  python3 run_story.py samples/story_deposit_en.txt          # one story
  python3 run_story.py samples/                              # every .txt in a folder
  python3 run_story.py my_story.txt --out reports            # choose output folder (default outputs/reports)

Each story becomes <out>/<name>.md. Works offline; if LAWYER_LLM is set it is NOT used here (kept deterministic)."""
import os, sys, glob
from lawyer.report import build_report
from lawyer import guard

args = [a for a in sys.argv[1:] if not a.startswith("--")]
out = "outputs/reports"
if "--out" in sys.argv:
    out = sys.argv[sys.argv.index("--out") + 1]
    args = [a for a in args if a != out]
if not args:
    sys.exit(__doc__)
files = []
for a in args:
    files += sorted(glob.glob(os.path.join(a, "*.txt"))) if os.path.isdir(a) else [a]
os.makedirs(out, exist_ok=True)
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    report, s = build_report(open(f, encoding="utf-8").read(), name)
    bad = guard.violations(report)
    open(os.path.join(out, name + ".md"), "w", encoding="utf-8").write(report + ("\n\nGUARD VIOLATIONS: " + str(bad) if bad else ""))
    print(f"{name}: topic={s.topic}, guard={'CLEAN' if not bad else bad}  -> {out}/{name}.md")
