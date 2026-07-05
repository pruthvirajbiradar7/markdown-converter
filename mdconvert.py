#!/usr/bin/env python3
"""
mdconvert.py - Convert files and folders to Markdown.
"""
import argparse
import sys
from pathlib import Path
from markitdown import MarkItDown
import image_ocr

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml", ".txt",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".mp3", ".wav", ".m4a", ".epub", ".zip",
}

def _pdf_to_markdown(path):
    try:
        import fitz
    except ImportError:
        raise ImportError("pymupdf not installed. Run install_pdf_support.bat.")
    doc = fitz.open(str(path))
    parts = [p for p in (page.get_text("text").strip() for page in doc) if p]
    doc.close()
    return "\n\n".join(parts) if parts else ""

def iter_input_files(paths, recursive):
    items = []
    for p in paths:
        if p.startswith("http://") or p.startswith("https://"):
            items.append(p)
            continue
        path = Path(p)
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            for f in sorted(path.glob(pattern)):
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
                    items.append(f)
        elif path.is_file():
            items.append(path)
        else:
            print(f"  [skip] not found: {p}", file=sys.stderr)
    return items

def convert_one(md_engine, item, outdir, to_stdout):
    label = item if isinstance(item, str) else item.name

    if not isinstance(item, str) and Path(item).suffix.lower() == ".pdf":
        try:
            text = _pdf_to_markdown(item)
        except Exception as e:
            print(f"  [FAIL] {label}: {e}", file=sys.stderr)
            return False
    else:
        try:
            result = md_engine.convert(str(item))
            text = result.text_content if hasattr(result, "text_content") else result.markdown
        except Exception as e:
            print(f"  [FAIL] {label}: {e}", file=sys.stderr)
            return False

    if not isinstance(item, str) and image_ocr.is_image(item):
        ocr_text = image_ocr.ocr_image(item)
        if ocr_text:
            label_line = "## Text detected in image (OCR)\n\n"
            text = (text.strip() + "\n\n" + label_line + ocr_text).strip() if text.strip() else (label_line + ocr_text)

    if to_stdout:
        print(f"\n{'='*10} {label} {'='*10}\n")
        print(text)
        return True

    if isinstance(item, str):
        stem = item.rstrip("/").split("/")[-1] or "page"
        stem = stem.rsplit(".", 1)[0]
        out_path = (outdir or Path(".")) / f"{stem}.md"
    else:
        target_dir = outdir if outdir else item.parent
        out_path = target_dir / f"{item.stem}.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"  [ok] {label} -> {out_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Convert files to Markdown.")
    parser.add_argument("inputs", nargs="+", help="Files, folders, or URLs")
    parser.add_argument("-o", "--outdir", type=Path, default=None)
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    items = iter_input_files(args.inputs, args.recursive)
    if not items:
        print("Nothing to convert.", file=sys.stderr)
        sys.exit(1)

    try:
        md_engine = MarkItDown(enable_plugins=False)
    except TypeError:
        md_engine = MarkItDown()

    ok, fail = 0, 0
    for item in items:
        if convert_one(md_engine, item, args.outdir, args.stdout):
            ok += 1
        else:
            fail += 1

    if not args.stdout:
        print(f"\nDone: {ok} converted, {fail} failed.")

if __name__ == "__main__":
    main()
