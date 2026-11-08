"""Terminal chat:  python3 cli.py"""
import sys

from lawyer.engine import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

s = Session()
print(s.say("hi")); print()
while True:
    try:
        m = input("you> ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if m:
        print("\nlawyer>", s.say(m), "\n")
