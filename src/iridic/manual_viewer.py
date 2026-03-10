from __future__ import annotations

from pathlib import Path
from typing import Dict, Literal, Optional, Union

import streamlit as st

from .manual.index import (
    ManualFile,
    TreeNode,
    build_manual_index,
    numeric_sort_key,
    render_generated_tree_text,
    search_manual,
)
from .manual.outline import ensure_manual_outline


OutlineMode = Literal["never", "if_missing", "always"]


@st.cache_data(show_spinner=False)
def build_manual_index_cached(manual_dir: str) -> tuple[TreeNode, Dict[str, ManualFile]]:
    return build_manual_index(manual_dir)


def _toggle_selected(rel_str: str) -> None:
    """
    Click once -> open and show indicator.
    Click again -> close and remove indicator.
    """
    if st.session_state.get("manual_selected") == rel_str:
        st.session_state.manual_selected = None
    else:
        st.session_state.manual_selected = rel_str

    st.rerun()


def _validate_outline_mode(mode: str) -> OutlineMode:
    allowed: set[str] = {"never", "if_missing", "always"}
    if mode not in allowed:
        raise ValueError(
            f"ensure_outline must be one of {sorted(allowed)}, got: {mode!r}"
        )
    return mode  # type: ignore[return-value]


def render_manual_ui(
    *,
    repo_root: Union[str, Path],
    manual_rel_dir: Union[str, Path] = "manual",
    expander_label: str = "📘 Show / Hide Instruction Manual",
    ensure_outline: OutlineMode = "if_missing",
    outline_title: str = "Instruction Manual",
    outline_version: str = "0.0.0",
    outline_max_depth: int | None = None,
) -> None:
    """
    Render a single-pane Streamlit manual viewer.

    Parameters
    ----------
    repo_root
        Repository root containing the manual directory.
    manual_rel_dir
        Manual directory relative to repo_root.
    expander_label
        Label for the top-level manual expander.
    ensure_outline
        Outline behavior:
        - "never": do not generate/check the outline
        - "if_missing": generate only if 00_outline.md is absent
        - "always": rebuild 00_outline.md on each render
    outline_title
        Title used if the outline is generated.
    outline_version
        Version string used if the outline is generated.
    outline_max_depth
        Optional max depth for the generated outline tree.
    """
    repo_root = Path(repo_root).resolve()
    manual_root = (repo_root / manual_rel_dir).resolve()
    ensure_outline = _validate_outline_mode(ensure_outline)

    if "manual_selected" not in st.session_state:
        st.session_state.manual_selected = None
    if "manual_expand_all" not in st.session_state:
        st.session_state.manual_expand_all = False
    if "manual_search" not in st.session_state:
        st.session_state.manual_search = ""

    if not manual_root.exists():
        st.warning(f"Manual directory not found: {manual_root}")
        return

    if ensure_outline != "never":
        try:
            ensure_manual_outline(
                manual_root,
                manual_title=outline_title,
                manual_version=outline_version,
                max_depth=outline_max_depth,
                if_missing_only=(ensure_outline == "if_missing"),
            )
        except Exception as exc:
            st.warning(f"Could not prepare manual outline: {exc}")

    tree, flat = build_manual_index_cached(str(manual_root))

    if not flat:
        st.warning(f"No markdown files found under: {manual_root}")
        return

    with st.expander(expander_label, expanded=False):
        c1, c2, c3 = st.columns([1, 1, 2])

        with c1:
            st.session_state.manual_expand_all = st.toggle(
                "Expand all",
                value=st.session_state.manual_expand_all,
            )

        with c2:
            if st.button("Hide section", key="section_hide"):
                st.session_state.manual_selected = None
                st.rerun()

        with c3:
            st.session_state.manual_search = st.text_input(
                "Search",
                value=st.session_state.manual_search,
                placeholder="Search titles + content…",
            )

        st.caption("Tip: Click a file once to show it below. Click it again to hide it.")

        with st.expander("🗂 Manual Map (Tree)", expanded=False):
            st.code(render_generated_tree_text(tree), language="text")

        q = st.session_state.manual_search.strip()
        if q:
            with st.expander("🔎 Search results", expanded=True):
                results = search_manual(flat, q, limit=25)
                if not results:
                    st.caption("No matches.")
                else:
                    for rel_str, _score in results:
                        mf = flat[rel_str]
                        if st.button(
                            f"📄 {mf.rel_path.as_posix()} — {mf.title}",
                            key=f"sr_{rel_str}",
                        ):
                            _toggle_selected(rel_str)

        st.markdown("### 📚 Manual Sections")

        root_keys = sorted(tree.keys(), key=numeric_sort_key)
        for name in root_keys:
            node = tree[name]
            if isinstance(node, dict):
                with st.expander(f"📁 {name}", expanded=st.session_state.manual_expand_all):
                    _render_folder_accordion(
                        node=node,
                        rel_prefix=Path(name),
                        flat=flat,
                        expand_all=st.session_state.manual_expand_all,
                    )
            else:
                rel_str = Path(name).as_posix()
                mf = flat.get(rel_str)

                label = f"📄 {name}"
                if mf and mf.title and mf.title != name:
                    label = f"📄 {name} — {mf.title}"

                if st.session_state.manual_selected == rel_str:
                    label = f"▶ {label}"

                if st.button(label, key=f"root_open_{rel_str}"):
                    _toggle_selected(rel_str)

    rel_selected: Optional[str] = st.session_state.manual_selected
    if not rel_selected:
        st.info("Select from the above menu to view instructions.")
        return

    if rel_selected not in flat:
        st.warning(f"Selected file not found: {rel_selected}")
        return

    mf = flat[rel_selected]
    crumbs = ["Manual"] + list(mf.rel_path.parts)
    st.caption(" / ".join(crumbs))
    st.markdown(f"## {mf.title}")
    st.markdown(mf.text)


def _render_folder_accordion(
    *,
    node: TreeNode,
    rel_prefix: Path,
    flat: Dict[str, ManualFile],
    expand_all: bool,
) -> None:
    keys = sorted(node.keys(), key=numeric_sort_key)
    for name in keys:
        child = node[name]

        if isinstance(child, dict):
            with st.expander(f"📁 {name}", expanded=expand_all):
                _render_folder_accordion(
                    node=child,
                    rel_prefix=rel_prefix / name,
                    flat=flat,
                    expand_all=expand_all,
                )
        else:
            rel_str = (rel_prefix / name).as_posix()
            mf = flat.get(rel_str)

            label = f"📄 {name}"
            if mf and mf.title and mf.title != name:
                label = f"📄 {name} — {mf.title}"

            if st.session_state.get("manual_selected") == rel_str:
                label = f"▶ {label}"

            if st.button(label, key=f"open_{rel_str}"):
                _toggle_selected(rel_str)
