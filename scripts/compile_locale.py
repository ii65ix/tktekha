"""Compile locale/ar/LC_MESSAGES/django.po to django.mo using polib (no GNU gettext required)."""
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent
PO = ROOT / "locale" / "ar" / "LC_MESSAGES" / "django.po"
MO = ROOT / "locale" / "ar" / "LC_MESSAGES" / "django.mo"


def main() -> None:
    if not PO.exists():
        raise SystemExit(f"Missing {PO}")
    po = polib.pofile(str(PO))
    MO.parent.mkdir(parents=True, exist_ok=True)
    po.save_as_mofile(str(MO))
    print("Wrote", MO)


if __name__ == "__main__":
    main()
