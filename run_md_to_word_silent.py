r"""
run_md_to_word_silent.py
Called by the right-click menu when a .md file is right-clicked
and "Convert to Word" is selected.
Converts the Markdown file to a .docx, saved next to the original.
All output is logged to %TEMP%\mdconvert_log.txt.
"""
import sys
import os

log_path = os.path.join(
    os.environ.get("TEMP", os.path.dirname(os.path.abspath(__file__))),
    "mdconvert_log.txt"
)

log_file = open(log_path, "w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    from pathlib import Path
    import md_to_docx

    if len(sys.argv) < 2:
        print("No file specified.")
        sys.exit(1)

    md_path = Path(sys.argv[1])

    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)

    docx_path = md_to_docx.convert_md_to_docx(md_path)
    print(f"[ok] {md_path.name} -> {docx_path.name}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    log_file.close()
