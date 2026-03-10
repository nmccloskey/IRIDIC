import yaml
import zipfile
import tempfile
from io import BytesIO
import streamlit as st
from pathlib import Path
import random, numpy as np
from datetime import datetime

from iridic import __version__
from iridic import render_manual_ui  

start_time = datetime.now()

# ------------------------------------------------------------------
# Path setup and zip utility
# ------------------------------------------------------------------
def add_src_to_sys_path():
    import sys
    src_path = Path(__file__).resolve().parent.parent / "src"
    sys.path.insert(0, str(src_path))
add_src_to_sys_path()

def zip_folder(folder_path: Path) -> BytesIO:
    """Compress the given folder into an in-memory ZIP buffer."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(folder_path)
                zf.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer

# ------------------------------------------------------------------
# Streamlit header
# ------------------------------------------------------------------
st.title("IRIDIC Web App")
st.subheader("Idiosyncratic Repository of Initialization and Development Itineraries for Codebases \n(a personal meta-repository)")
st.subheader(f"version: {__version__}")

# ------------------------------------------------------------------
# Instruction manual toggle
# ------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]  # webapp/ -> REPO/

render_manual_ui(
    repo_root=REPO_ROOT,
    manual_rel_dir="manual",
    expander_label="📘 Show / Hide IRIDIC Manual Menu",
)


# # ---------------------------------------------------------------
# # PART 2: INPUT FILES
# # ---------------------------------------------------------------
# st.header("Upload input files")
# md_files = st.file_uploader("Upload input files", type=["md"], accept_multiple_files=True)

# with tempfile.TemporaryDirectory() as tmpdir:
#     root_dir = Path(tmpdir).resolve()

#     input_dir = (root_dir / "input").resolve()
#     output_dir = (root_dir / "output").resolve()
#     input_dir.mkdir(exist_ok=True)
#     output_dir.mkdir(exist_ok=True)

#     # Save uploaded input files
#     for file in md_files:
#         file_path = input_dir / file.name
#         with file_path.open("wb") as f:
#             f.write(file.read())

#     # Create timestamped output folder and logger
#     timestamp = start_time.strftime("%y%m%d_%H%M")
#     out_dir = (output_dir / f"diaad_output_{timestamp}").resolve()
#     out_dir.mkdir(parents=True, exist_ok=True)

#     # ---------------------------------------------------------------
#     # PART 3: FUNCTION SELECTION
#     # ---------------------------------------------------------------
#     st.header("Part 3: Select function(s) to run")
#     all_functions = [
#     ]

#     selected_funcs = st.multiselect("Select functions", all_functions)

#     if st.button("Run selected functions"):
#         if not selected_funcs:
#             st.warning("Please select at least one function.")
#             st.stop()

#         try:

#             # --- Execute selected functions ---
#             for func in selected_funcs:
#                 ...


#             st.success("✅ All selected functions completed successfully!")

#         except Exception as e:
#             st.error(
#                 "❌ An unexpected error occurred while running IRIDIC. "
#                 "Please check the logs in the downloaded ZIP for details."
#             )


#         # --- Create timestamped ZIP for download ---
#         timestamp = start_time.strftime("%y%m%d_%H%M")
#         zip_buffer = zip_folder(out_dir)
#         st.download_button(
#             label="⬇️ Download Results ZIP",
#             data=zip_buffer,
#             file_name=f"diaad_web_output_{timestamp}.zip",
#             mime="application/zip"
#         )

def main():
    """Launch this file as a Streamlit app."""
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])
