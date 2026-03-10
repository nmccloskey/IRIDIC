from __future__ import annotations

import zipfile
from datetime import datetime
from io import BytesIO
from pathlib import Path

import streamlit as st

from iridic import __version__
from iridic.webapp.manual_viewer import render_manual_ui


def zip_folder(folder_path: Path) -> BytesIO:
    """Compress a folder into an in-memory ZIP buffer."""
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(folder_path)
                zf.write(file_path, arcname)

    zip_buffer.seek(0)
    return zip_buffer


def get_repo_root() -> Path:
    """
    Return the repository root.

    Expected file location:
        repo_root/src/iridic/webapp/streamlit_app.py
    """
    return Path(__file__).resolve().parents[3]


def main() -> None:
    """Run the IRIDIC Streamlit app."""
    start_time = datetime.now()
    repo_root = get_repo_root()

    st.set_page_config(
        page_title="IRIDIC Web App",
        page_icon="📘",
        layout="wide",
    )

    st.title("IRIDIC Web App")
    st.subheader(
        "Idiosyncratic Repository of Initialization and Development "
        "Itineraries for Codebases"
    )
    st.caption("(a personal meta-repository)")
    st.caption(f"Version: {__version__}")

    render_manual_ui(
        repo_root=repo_root,
        manual_rel_dir="docs/manual",
        expander_label="📘 Show / Hide IRIDIC Manual Menu",
    )

    # Placeholder body content
    st.markdown("---")
    st.write("Welcome to the IRIDIC web app.")

    elapsed = datetime.now() - start_time
    st.caption(f"App loaded in {elapsed.total_seconds():.2f} seconds.")


if __name__ == "__main__":
    main()
