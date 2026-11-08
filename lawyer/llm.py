"""Swappable LLM adapter (stdlib only). Off by default.

  LAWYER_LLM   = none | gemini | openai | anthropic     (default none)
  LAWYER_MODEL = model name (optional, sensible default per provider)
  GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY
  OPENAI_BASE_URL (optional; any OpenAI-compatible endpoint, e.g. a local server)

The LLM never writes legal content. It only (a) translates a user message into
English and (b) rewrites an already-grounded answer into simple words in the
user's language. Both outputs pass through guard.accept_rewrite().
"""
import json, os, urllib.error, urllib.request

DEFAULT_MODEL = {"gemini": "gemini-3.6-flash", "openai": "gpt-4o-mini", "anthropic": "claude-haiku-5-5"}


class LLMError(RuntimeError):
    pass


REWRITE_SYSTEM = (
    "You rewrite a legal information message for an ordinary person in India. "
    "Rules: write in {lang}; use short plain sentences; keep every fact, number, helpline and "
    "bullet from the source; DO NOT add any law, Act, Section number, case, court name, deadline "
    "or number that is not in the source; do not give new advice; keep Act names exactly as written. "
    "Output only the rewritten message.")
TRANSLATE_SYSTEM = "Translate the user's message to English. Output only the translation."


def _post(url, payload, headers):
    req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise LLMError(f"HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise LLMError("network connection failed") from e
    except json.JSONDecodeError as e:
        raise LLMError("invalid response from provider") from e


class Provider:
    name = "none"

    def complete(self, system, user):  # pragma: no cover
        raise NotImplementedError


class Gemini(Provider):
    name = "gemini"

    def __init__(self, model, key):
        self.model, self.key = model, key

    def complete(self, system, user):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        d = _post(url, {"system_instruction": {"parts": [{"text": system}]},
                        "contents": [{"role": "user", "parts": [{"text": user}]}]},
                  {"x-goog-api-key": self.key})
        try:
            return d["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as e:
            raise LLMError("invalid response from Gemini") from e


class OpenAI(Provider):
    name = "openai"

    def __init__(self, model, key, base):
        self.model, self.key, self.base = model, key, base

    def complete(self, system, user):
        d = _post(self.base.rstrip("/") + "/chat/completions",
                  {"model": self.model, "messages": [{"role": "system", "content": system},
                                                     {"role": "user", "content": user}]},
                  {"Authorization": "Bearer " + self.key})
        return d["choices"][0]["message"]["content"]


class Anthropic(Provider):
    name = "anthropic"

    def __init__(self, model, key):
        self.model, self.key = model, key

    def complete(self, system, user):
        d = _post("https://api.anthropic.com/v1/messages",
                  {"model": self.model, "max_tokens": 2000, "system": system,
                   "messages": [{"role": "user", "content": user}]},
                  {"x-api-key": self.key, "anthropic-version": "2023-06-01"})
        return d["content"][0]["text"]


def from_env():
    name = os.environ.get("LAWYER_LLM", "none").lower()
    if name == "none":
        return None
    key_names = {"gemini": "GEMINI_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY"}
    if name not in key_names:
        raise ValueError("unknown LAWYER_LLM: " + name)
    key_name = key_names[name]
    key = os.environ.get(key_name)
    if not key:
        raise RuntimeError(f"{key_name} is required when LAWYER_LLM={name}. Set it in your environment; do not put it in source files.")
    model = os.environ.get("LAWYER_MODEL", DEFAULT_MODEL.get(name, ""))
    if name == "gemini":
        return Gemini(model, key)
    if name == "openai":
        return OpenAI(model, key, os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    if name == "anthropic":
        return Anthropic(model, key)
