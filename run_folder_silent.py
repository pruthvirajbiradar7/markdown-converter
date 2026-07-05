r"""
run_folder_silent.py
Called by the right-click menu when a folder is right-clicked and
"Convert to Markdown" is selected.

Shows a confirmation dialog with the file count, then silently converts
all supported files in that folder. MD files appear next to the originals.
Original files are never moved or deleted.
"""
import sys
import os

# Make sure this script's folder is on the path so mdconvert and image_ocr are found
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml", ".txt",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".mp3", ".wav", ".m4a",
    ".epub", ".zip",
}


def show_dialog(title, message, kind="yesno"):
    """Show a native Windows dialog using tkinter (built into Python)."""
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes("-topmost", True)
        if kind == "yesno":
            result = messagebox.askyesno(title, message, parent=root)
        else:
            messagebox.showinfo(title, message, parent=root)
            result = None
        root.destroy()
        return result
    except Exception:
        # tkinter unavailable — proceed without dialog
        return True


# --- Entry point ---

if len(sys.argv) < 2:
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.isdir(folder_path):
    sys.exit(1)

# Count supported files in the folder (top-level only — not subfolders)
files_to_convert = [
    f for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
    and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
]

count = len(files_to_convert)
folder_name = os.path.basename(folder_path)

if count == 0:
    show_dialog(
        "Convert to Markdown",
        f"No supported files found in:\n\n{folder_name}\n\nNothing to convert.",
        kind="info",
    )
    sys.exit(0)

# --- Confirmation dialog ---
confirmed = show_dialog(
    "Convert to Markdown",
    f"Convert {count} file{'s' if count != 1 else ''} in '{folder_name}' to Markdown?\n\n"
    f"Each .md file will appear right next to the original.\n"
    f"Original files will not be moved or deleted."
)

if not confirmed:
    sys.exit(0)

# --- Silent conversion ---
log_path = os.path.join(
    os.environ.get("TEMP", script_dir),
    "mdconvert_log.txt"
)

log_file = open(log_path, "w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

try:
    import mdconvert
    sys.argv = ["mdconvert.py", folder_path]
    mdconvert.main()
except Exception as e:
    print(f"Fatal error: {e}", flush=True)
    import traceback
    traceback.print_exc()
finally:
    log_file.close()
