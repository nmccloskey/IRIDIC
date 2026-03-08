"""
IRIDIC package.

Utilities for indexing, viewing, validating, and compiling project manuals.
"""

from importlib.metadata import PackageNotFoundError, version

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
from .manual_outline import (
    build_manual_outline,
    ensure_manual_outline,
)
from .manual_chars import (
    Finding,
    CharScanResult,
    check_manual_chars,
)
from .manual_pdf import (
    build_manual_pdf,
)

__all__ = [
    "ManualFile",
    "TreeNode",
    "Finding",
    "CharScanResult",
    "build_manual_index",
    "extract_md_title",
    "numeric_sort_key",
    "read_text_safely",
    "render_generated_tree_text",
    "search_manual",
    "build_manual_outline",
    "ensure_manual_outline",
    "check_manual_chars",
    "build_manual_pdf",
]

try:
    __version__ = version("iridic")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"