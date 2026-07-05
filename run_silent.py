r"""
run_silent.py - Called by right-click on a FILE. Runs silently via pythonw.exe.
"""
import sys
import os

log_path = os.path.join(os.environ.get("TEMP", os.path.dirname(os.path.abspath(__file__))), "mdconvert_log.txt")
log_file = open(log_path, "w", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    import mdconvert
    mdconvert.main()
except Exception as e:
    print(f"Fatal error: {e}", flush=True)
    import traceback
    traceback.print_exc()
finally:
    log_file.close()
