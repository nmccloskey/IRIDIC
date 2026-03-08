"""
IRIDIC package.

Utilities for indexing, viewing, validating, and compiling project manuals.
"""

from .manual_index import (
    ManualFile,
    TreeNode,
    build_manual_index,
    extract_md_title,
    numeric_sort_key,
    read_text_safely,
    render_generated_tree_text,
    search_manual,
)
from .manual_viewer import (
    render_manual_ui,
    render_manual_ui_single_pane,
)

__all__ = [
    "ManualFile",
    "TreeNode",
    "build_manual_index",
    "extract_md_title",
    "numeric_sort_key",
    "read_text_safely",
    "render_generated_tree_text",
    "search_manual",
    "render_manual_ui",
    "render_manual_ui_single_pane",
]

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("iridic")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"