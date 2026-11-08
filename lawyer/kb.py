"""Closed knowledge base loader. The only source of legal statements."""
import json, os

_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "sources.json")
with open(_PATH, encoding="utf-8") as f:
    ENTRIES = {e["id"]: e for e in json.load(f)["entries"]}


def get(eid):
    return ENTRIES[eid]


def for_topic(topic):
    return [e for e in ENTRIES.values() if e["topic"] == topic]


def allowed_acts():
    acts = set()
    for e in ENTRIES.values():
        acts.update(a.lower() for a in e["acts"])
    return acts


def allowed_sections():
    """{(section_no_lower, act_lower)}"""
    out = set()
    for e in ENTRIES.values():
        for s in e["sections"]:
            out.add((s["n"].lower(), s["act"].lower()))
    return out
