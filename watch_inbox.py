#!/usr/bin/env python3
"""
watch_inbox.py - Watch a folder; anything dropped in gets auto-converted to Markdown.
Usage:
    python watch_inbox.py                      # watches ~/markdown-inbox
    python watch_inbox.py --folder C:\MyInbox
    python watch_inbox.py --archive            # move originals to processed/ after converting
"""
import argparse
import shutil
import sys
import time
from pathlib import Path
from markitdown import MarkItDown
import image_ocr

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml", ".txt",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".mp3", ".wav", ".m4a", ".epub", ".zip",
}
POLL_SECONDS = 2

def settle(path):
    try:
        size1 = path.stat().st_size
        time.sleep(0.5)
        size2 = path.stat().st_size
        return size1 == size2
    except FileNotFoundError:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path, default=Path.home() / "markdown-inbox")
    parser.add_argument("--archive", action="store_true")
    args = parser.parse_args()

    inbox = args.folder
    converted_dir = inbox / "converted"
    processed_dir = inbox / "processed"
    inbox.mkdir(parents=True, exist_ok=True)
    converted_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)

    try:
        md_engine = MarkItDown(enable_plugins=False)
    except TypeError:
        md_engine = MarkItDown()

    print(f"Watching: {inbox}")
    print(f"Converted files -> {converted_dir}")
    print("Press Ctrl+C to stop.\n")

    seen = set()
    try:
        while True:
            for f in sorted(inbox.iterdir()):
                if not f.is_file() or f.suffix.lower() not in SUPPORTED_EXTENSIONS or f in seen:
                    continue
                if not settle(f):
                    continue

                out_path = converted_dir / f"{f.stem}.md"
                try:
                    if f.suffix.lower() == ".pdf":
                        import fitz
                        doc = fitz.open(str(f))
                        parts = [p for p in (page.get_text("text").strip() for page in doc) if p]
                        doc.close()
                        text = "\n\n".join(parts)
                    else:
                        result = md_engine.convert(str(f))
                        text = result.text_content if hasattr(result, "text_content") else result.markdown

                    if image_ocr.is_image(f):
                        ocr_text = image_ocr.ocr_image(f)
                        if ocr_text:
                            label = "## Text detected in image (OCR)\n\n"
                            text = (text.strip() + "\n\n" + label + ocr_text).strip() if text.strip() else (label + ocr_text)

                    out_path.write_text(text, encoding="utf-8")
                    print(f"[ok] {f.name} -> converted/{out_path.name}")
                    if args.archive:
                        shutil.move(str(f), str(processed_dir / f.name))
                except Exception as e:
                    print(f"[FAIL] {f.name}: {e}", file=sys.stderr)
                seen.add(f)
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
