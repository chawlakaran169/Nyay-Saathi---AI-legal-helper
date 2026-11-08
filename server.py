"""Zero-dependency web app:  python3 server.py   ->  http://localhost:8000"""
import html, json, os, re, uuid
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from lawyer.engine import Session
from lawyer import llm as llm_mod

SESSIONS = {}
HERE = os.path.dirname(os.path.abspath(__file__))
LLM_PROVIDER = "none"
BUILD_ID = "punjabi-translation-v2"


def printable(text, sid, kind):
    body = html.escape(text)
    body = re.sub(r"^### (.*)$", r"<h3>\1</h3>", body, flags=re.M)
    body = re.sub(r"^# (.*)$", r"<h2>\1</h2>", body, flags=re.M)
    body = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", body)
    return ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Nyay Saathi: " + kind + "</title>"
            "<style>body{font:15px/1.55 system-ui,'Noto Sans Devanagari',sans-serif;max-width:760px;margin:0 auto;padding:16px;color:#1d2433;background:#fff}"
            "div.t{white-space:pre-wrap}h2,h3{color:#1f5f4a}.bar{display:flex;gap:10px;margin-bottom:12px}"
            "a,button{padding:8px 12px;border:1px solid #bbb;border-radius:8px;background:#fff;color:#1d2433;text-decoration:none;font:inherit;cursor:pointer}"
            "@media print{.bar{display:none}}</style>"
            f"<div class=bar><button onclick='window.print()'>Print / Save as PDF</button><a href='/export?sid={sid}&kind={kind}&fmt=txt'>Download .txt</a></div>"
            f"<div class=t>{body}</div>")


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/health":
            self._send(200, json.dumps({"build": BUILD_ID, "llm": LLM_PROVIDER}))
        elif u.path in ("/", "/index.html"):
            self._send(200, open(os.path.join(HERE, "web", "index.html"), "rb").read(), "text/html")
        elif u.path == "/dashboard":
            f = os.path.join(HERE, "outputs", "dashboard.html")
            self._send(200, open(f, "rb").read() if os.path.exists(f) else b"Run: python3 tests/run_tests.py", "text/html")
        elif u.path == "/export":
            q = parse_qs(u.query)
            s = SESSIONS.get((q.get("sid") or [""])[0])
            kind = (q.get("kind") or ["summary"])[0]
            text = s.export(kind) if s else "Session not found."
            if kind == "calendar" and s:
                data = text.encode("utf-8")
                self.send_response(200); self.send_header("Content-Type", "text/calendar; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="nyay-saathi-reminders.ics"')
                self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            elif (q.get("fmt") or [""])[0] == "txt":
                data = text.replace("**", "").replace("### ", "").replace("# ", "").encode("utf-8")
                self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="nyay-saathi-{kind}.txt"')
                self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            else:
                self._send(200, printable(text, (q.get("sid") or [""])[0], kind), "text/html")
        else:
            self._send(404, "{}")

    def do_POST(self):
        if self.path != "/api/chat":
            return self._send(404, "{}")
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or "{}")
        sid = body.get("session") or uuid.uuid4().hex
        s = SESSIONS.setdefault(sid, Session())
        msg = (body.get("message") or "").strip()[:4000]
        reply = s.say(msg) if msg else ""
        self._send(200, json.dumps({"session": sid, "reply": reply, "lang": s.lang, "violations": s.meta["violations"], "exports": s.exports_available()}))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    try:
        configured_llm = llm_mod.from_env()
    except (RuntimeError, ValueError) as e:
        raise SystemExit(f"AI configuration error: {e}") from e
    LLM_PROVIDER = configured_llm.name if configured_llm else "none"
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(("0.0.0.0", port), H)
    print(f"AI Lawyer running at http://localhost:{port}  (LLM: {os.environ.get('LAWYER_LLM', 'none')})")
    server.serve_forever()
