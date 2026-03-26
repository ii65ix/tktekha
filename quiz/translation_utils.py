"""Translate English quiz strings to Arabic (for DB fields text_ar / option*_ar)."""

from __future__ import annotations

import time
from contextlib import contextmanager

import requests


@contextmanager
def _requests_default_timeout(timeout: float = 25.0):
    """
    deep-translator calls requests.get() without a timeout, which can hang on bad networks.
    Temporarily patch requests.get to add a default timeout (management command only).
    """
    _orig = requests.get

    def _get(*args, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = timeout
        return _orig(*args, **kwargs)

    requests.get = _get
    try:
        yield
    finally:
        requests.get = _orig


def _translate_google(text: str, *, max_chars: int) -> str:
    from deep_translator import GoogleTranslator

    text = str(text).strip()[:max_chars]
    with _requests_default_timeout(25.0):
        translator = GoogleTranslator(source="en", target="ar")
        return translator.translate(text)


def _translate_mymemory_chunked(text: str, *, max_chars: int) -> str:
    """MyMemory allows ~500 chars per request; chunk and join."""
    from deep_translator import MyMemoryTranslator

    text = str(text).strip()[:max_chars]
    if not text:
        return ""
    chunk_size = 480
    parts: list[str] = []
    with _requests_default_timeout(25.0):
        translator = MyMemoryTranslator(source="en", target="ar")
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size].strip()
            if not chunk:
                continue
            time.sleep(0.05)
            parts.append(translator.translate(chunk))
    return " ".join(parts).strip()


def translate_en_to_ar(
    text: str,
    *,
    max_chars: int = 4500,
    retries: int = 3,
) -> str:
    """
    Translate English → Arabic. Tries Google first, then MyMemory.
    Returns "" on empty input or if all attempts fail.
    """
    if not text or not str(text).strip():
        return ""

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            result = _translate_google(text, max_chars=max_chars)
            if result:
                return result
        except KeyboardInterrupt:
            raise
        except Exception as e:
            last_error = e
            time.sleep(1.0 * (attempt + 1))

    try:
        return _translate_mymemory_chunked(text, max_chars=max_chars)
    except KeyboardInterrupt:
        raise
    except Exception:
        if last_error:
            pass
        return ""


def translate_question_fields(
    question,
    *,
    force: bool = False,
    option_max_len: int = 512,
) -> list[str]:
    """
    Set Arabic fields on a Question instance. Returns list of field names updated.
    Does not call save().
    """
    updated: list[str] = []

    if force or not (question.text_ar or "").strip():
        time.sleep(0.06)
        ar = translate_en_to_ar(question.text)
        if ar:
            question.text_ar = ar
            updated.append("text_ar")

    for i in range(1, 5):
        en = getattr(question, f"option{i}", "") or ""
        ar_field = f"option{i}_ar"
        current = getattr(question, ar_field, "") or ""
        if force or not current.strip():
            time.sleep(0.06)
            ar = translate_en_to_ar(en, max_chars=600)
            if ar:
                setattr(question, ar_field, ar[:option_max_len])
                updated.append(ar_field)

    return updated
