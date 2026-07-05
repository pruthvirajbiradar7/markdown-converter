# Local File-to-Markdown Converter

Convert PDFs, Word docs, PowerPoint, Excel, images, HTML, and more into clean
Markdown — entirely on your own PC. No uploads, no browser, no internet required
after setup. Right-click any file or folder to convert.

Built on [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft,
with [PyMuPDF](https://pymupdf.readthedocs.io/) for robust PDF extraction and
[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) for reading
text inside images.

---

## Why this exists

Most AI tools work best when given information in Markdown format. Converting
files one-by-one through web services is slow and requires uploading private
documents to the internet. This tool does it locally, instantly, and privately.

---

## Features

- **Right-click any file** to convert it silently — no window, no popup,
  the `.md` file appears next to the original in seconds
- **Right-click any folder** to convert all supported files inside it at once,
  with a confirmation dialog showing how many files will be converted
- **Auto-watched inbox folder** — drop files in, get Markdown out automatically
- **OCR support** — reads text labels and content from images and diagrams
  (requires free Tesseract install)
- Completely **offline and private** — nothing leaves your PC
- Works on **Windows 10/11** (Mac/Linux supported via command line)

---

## Supported File Types

| Format | Extensions |
|---|---|
| PDF | `.pdf` |
| Word | `.docx`, `.doc` |
| PowerPoint | `.pptx`, `.ppt` |
| Excel | `.xlsx`, `.xls` |
| HTML | `.html`, `.htm` |
| Data files | `.csv`, `.json`, `.xml` |
| Plain text | `.txt` |
| Images (with OCR) | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp` |
| Audio (transcribed) | `.mp3`, `.wav`, `.m4a` |
| Other | `.epub`, `.zip` |

---

## Installation (Windows)

### Prerequisites
- **Python 3.10 or newer** — download from [python.org](https://www.python.org/downloads/)
  - During install, tick **"Add python.exe to PATH"**
  - Restart your PC after installing
- **Tesseract OCR** *(optional, for image text extraction)* — download from
  [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), install with
  default options

### Setup (one time, about 2 minutes)

1. Download this repository as a ZIP (green "Code" button above → "Download ZIP")
2. Extract to a permanent location, e.g. `Documents\markdown-converter`
3. Double-click **`setup.bat`** — installs all dependencies into a local `venv` folder
4. Double-click **`test_converter.bat`** — confirms everything is working
5. Double-click **`install_right_click_menu.bat`** — adds "Convert to Markdown"
   to your right-click menu for both files and folders

### Mac / Linux
```bash
chmod +x setup.sh
./setup.sh
./venv/bin/python mdconvert.py somefile.pdf
```

---

## Usage

### Right-click a file
Right-click any supported file in File Explorer → **"Convert to Markdown"**

The `.md` file appears silently next to the original within a few seconds.
No window, no popup — conversion happens in the background.

### Right-click a folder
Right-click any folder → **"Convert to Markdown"**

A dialog appears showing how many files will be converted and asking you to
confirm. Click Yes and all supported files in the folder are converted silently.
Each `.md` file appears next to its original.

### Auto-watched inbox folder
Double-click **`start_watcher.bat`** and leave it running. Drop files into
`~/markdown-inbox` and they convert automatically within seconds.
Results appear in `~/markdown-inbox/converted/`.

### Command line
```bash
# Convert one file
python mdconvert.py report.pdf

# Convert multiple files
python mdconvert.py report.pdf slides.pptx data.xlsx

# Convert a whole folder
python mdconvert.py ./my_folder

# Save all outputs to one place
python mdconvert.py ./my_folder -o ./markdown_output

# Convert a URL
python mdconvert.py https://example.com/page.html
```

---

## Troubleshooting

**Right-click menu not appearing:** Restart File Explorer (Task Manager →
Windows Explorer → Restart) or restart your PC.

**File converted but .md is empty:** The file may be a scanned/image-based PDF.
Install Tesseract OCR (see prerequisites) to extract text from images.

**Conversion failed silently:** Press `Win+R`, type `%TEMP%`, open
`mdconvert_log.txt` — it contains the full error from the most recent attempt.

**Moved the folder:** Re-run `install_right_click_menu.bat` to update the
registry to the new location.

---

## Project Structure

```
markdown-converter/
├── mdconvert.py              # Core conversion engine (CLI)
├── watch_inbox.py            # Folder watcher for auto-conversion
├── run_silent.py             # Called by right-click on files
├── run_folder_silent.py      # Called by right-click on folders
├── image_ocr.py              # OCR helper for images
├── install_right_click_menu.bat  # Adds right-click menu (files + folders)
├── uninstall_right_click_menu.bat
├── setup.bat / setup.sh      # One-time dependency install
├── test_converter.bat        # Verify everything works
├── install_pdf_support.bat   # Fix PDF support if needed
├── start_watcher.bat / .sh   # Launch the inbox watcher
├── requirements.txt
└── README.md
```

---

## License

MIT — free to use, modify, and share. See [LICENSE](LICENSE).

---

## Author

Built by Pruthvi Raj Biradar as a personal productivity tool for working with AI systems
that read Markdown.
