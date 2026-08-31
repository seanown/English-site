#!/usr/bin/env python3
"""Convert all images under img/ to WebP and rewrite HTML references.

Excludes:
- absolute URLs (https://...) -> not matched by the relative regex
- root-level files (avatar.jpg, favicon.svg) -> not under img/
Keeps originals only if conversion fails.
"""
import os, re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
HTML_FILES = sorted(ROOT.glob("*.html"))

def convert_one(src: Path):
    dst = src.with_suffix(".webp")
    try:
        im = Image.open(src)
        # preserve orientation from EXIF
        try:
            exif = im.getexif()
            ori = exif.get(0x0112, 1)
            if ori in (2,4,5,7):
                im = ImageOps.exif_transpose(im)
        except Exception:
            pass
        # RGBA -> RGB for webp simplicity (webp supports alpha but jpg sources are RGB)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(dst, "WEBP", quality=82, method=6)
        return dst
    except Exception as e:
        print(f"  FAIL {src.name}: {e}")
        return None

def main():
    # 1) convert
    converted, failed = [], []
    for src in sorted(IMG.rglob("*")):
        if src.suffix.lower() in (".jpg", ".jpeg", ".png"):
            dst = convert_one(src)
            if dst and dst.exists():
                converted.append((src, dst))
            else:
                failed.append(src)
    print(f"[convert] {len(converted)} ok, {len(failed)} failed")

    # 2) rewrite HTML refs (relative img/... only)
    pat = re.compile(r'(img/[^\"\'\s>]+?)\.(jpg|jpeg|png)(?=[\"\'\s>])', re.IGNORECASE)
    total_repl = 0
    for hf in HTML_FILES:
        txt = hf.read_text(encoding="utf-8")
        n = len(pat.findall(txt))
        if n == 0:
            continue
        new = pat.sub(lambda m: m.group(1) + ".webp", txt)
        hf.write_text(new, encoding="utf-8")
        total_repl += n
        print(f"  {hf.name}: {n} refs -> .webp")
    print(f"[refs] {total_repl} references rewritten across {len(HTML_FILES)} html files")

    # 3) remove originals (only those successfully converted)
    removed = 0
    for src, dst in converted:
        try:
            # sanity: dst must be valid webp
            with Image.open(dst) as t:
                assert t.format == "WEBP"
            src.unlink()
            removed += 1
        except Exception as e:
            print(f"  KEEP {src.name} (verify failed: {e})")
    print(f"[cleanup] removed {removed} originals")

    # 4) verify no leftover relative jpg/png refs
    leftover = 0
    for hf in HTML_FILES:
        txt = hf.read_text(encoding="utf-8")
        for m in re.finditer(r'(img/[^\"\'\s>]+?)\.(jpg|jpeg|png)', txt, re.IGNORECASE):
            # ignore if file still exists (shouldn't happen)
            p = ROOT / m.group(1) + "." + m.group(2).lower()
            if p.exists():
                print(f"  LEFTOVER EXISTING: {hf.name} -> {m.group(0)}")
                leftover += 1
    print(f"[verify] leftover existing-originals referenced: {leftover}")

if __name__ == "__main__":
    main()
