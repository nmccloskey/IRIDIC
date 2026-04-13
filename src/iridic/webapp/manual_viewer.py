from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, Literal, Optional, Union

import streamlit as st

from ..manual.index import (
    ManualFile,
    TreeNode,
    build_manual_index,
    numeric_sort_key,
    render_generated_tree_text,
    search_manual,
)
from ..manual.outline import ensure_manual_outline

OutlineMode = Literal["never", "if_missing", "always"]
_SECTION_LABEL_RE = re.compile(r"^(?P<num>\d+(?:[_-]\d+)*)(?:[_-].*)?$")


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


def _format_section_label(mf: ManualFile | None, fallback_name: str) -> str:
    name = mf.rel_path.name if mf else fallback_name
    stem = Path(name).stem
    title = mf.title if mf else fallback_name

    match = _SECTION_LABEL_RE.match(stem)
    if not match:
        return title

    section_num = ".".join(
        str(int(part)) for part in re.split(r"[_-]", match.group("num"))
    )
    return f"{section_num}: {title}"


def _manual_ui_namespace(manual_rel_dir: Union[str, Path], ui_key: str | None = None) -> str:
    """
    Return a stable namespace for one manual viewer instance.
    """
    if ui_key:
        base = ui_key
    else:
        base = Path(manual_rel_dir).as_posix()

    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", base).strip("_").lower()
    return safe or "manual"


def _manual_state_keys(ns: str) -> dict[str, str]:
    """
    Return namespaced session-state keys for one manual viewer instance.
    """
    return {
        "selected": f"{ns}_selected",
        "expand_all": f"{ns}_expand_all",
        "search": f"{ns}_search",
    }


def _init_manual_state(state_keys: dict[str, str]) -> None:
    """
    Initialize namespaced manual state if missing.
    """
    if state_keys["selected"] not in st.session_state:
        st.session_state[state_keys["selected"]] = None
    if state_keys["expand_all"] not in st.session_state:
        st.session_state[state_keys["expand_all"]] = False
    if state_keys["search"] not in st.session_state:
        st.session_state[state_keys["search"]] = ""


def _toggle_selected(selected_key: str, rel_str: str) -> None:
    """
    Toggle the visible manual section for a specific manual viewer.
    """
    current = st.session_state.get(selected_key)
    st.session_state[selected_key] = None if current == rel_str else rel_str


def _prepare_manual_root(
    *,
    repo_root: Union[str, Path],
    manual_rel_dir: Union[str, Path],
    ensure_outline: OutlineMode,
    outline_title: str,
    outline_version: str,
    outline_max_depth: int | None,
) -> Path | None:
    """
    Resolve manual root and ensure outline if requested.
    """
    repo_root = Path(repo_root).resolve()
    manual_root = (repo_root / manual_rel_dir).resolve()
    ensure_outline = _validate_outline_mode(ensure_outline)

    if not manual_root.exists():
        st.warning(f"Manual directory not found: {manual_root}")
        return None

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

    return manual_root


def _render_manual_controls(
    *,
    ns: str,
    state_keys: dict[str, str],
) -> None:
    """
    Render the top-row manual controls.
    """
    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        st.session_state[state_keys["expand_all"]] = st.toggle(
            "Expand all",
            value=st.session_state[state_keys["expand_all"]],
            key=f"{ns}_toggle_expand_all",
        )

    with c2:
        if st.button("Hide section", key=f"{ns}_hide_section"):
            st.session_state[state_keys["selected"]] = None
            st.rerun()

    with c3:
        st.session_state[state_keys["search"]] = st.text_input(
            "Search",
            value=st.session_state[state_keys["search"]],
            placeholder="Search titles + content...",
            key=f"{ns}_search_input",
        )

    st.caption("Tip: Click a file once to show it below. Click it again to hide it.")


def _render_manual_search(
    *,
    ns: str,
    flat,
    state_keys: dict[str, str],
) -> None:
    """
    Render search results for a manual viewer.
    """
    q = st.session_state[state_keys["search"]].strip()
    if not q:
        return

    with st.expander("Search results", expanded=True):
        results = search_manual(flat, q, limit=25)
        if not results:
            st.caption("No matches.")
            return

        for rel_str, _score in results:
            mf = flat[rel_str]
            label = _format_section_label(mf, mf.rel_path.name)
            if st.button(label, key=f"{ns}_search_result_{rel_str}"):
                _toggle_selected(state_keys["selected"], rel_str)


def _render_manual_sections(
    *,
    ns: str,
    tree,
    flat,
    state_keys: dict[str, str],
) -> None:
    """
    Render the manual section browser.
    """
    st.markdown("### Manual Sections")
    expand_all = st.session_state[state_keys["expand_all"]]
    selected = st.session_state[state_keys["selected"]]

    root_keys = sorted(tree.keys(), key=numeric_sort_key)
    for name in root_keys:
        node = tree[name]

        if isinstance(node, dict):
            with st.expander(
                f"Folder: {name}",
                expanded=expand_all,
            ):
                _render_folder_accordion(
                    node=node,
                    rel_prefix=Path(name),
                    flat=flat,
                    expand_all=expand_all,
                    selected_key=state_keys["selected"],
                    key_prefix=f"{ns}_folder",
                )
            continue

        rel_str = Path(name).as_posix()
        mf = flat.get(rel_str)
        label = _format_section_label(mf, name)

        if selected == rel_str:
            label = f"> {label}"

        if st.button(label, key=f"{ns}_root_open_{rel_str}"):
            _toggle_selected(state_keys["selected"], rel_str)


def _render_manual_content(*, flat, state_keys: dict[str, str], header_label: str = "Manual") -> None:
    """
    Render the selected manual section content below the menu.
    """
    rel_selected: Optional[str] = st.session_state[state_keys["selected"]]
    if not rel_selected:
        st.info("Select from the above menu to view instructions.")
        return

    if rel_selected not in flat:
        st.warning(f"Selected file not found: {rel_selected}")
        return

    mf = flat[rel_selected]
    crumbs = [header_label] + list(mf.rel_path.parts)
    st.caption(" / ".join(crumbs))
    st.markdown(mf.text)


def render_manual_ui(
    *,
    repo_root: Union[str, Path],
    manual_rel_dir: Union[str, Path] = "manual",
    expander_label: str = "Show / Hide Instruction Manual",
    ensure_outline: OutlineMode = "if_missing",
    outline_title: str = "Instruction Manual",
    outline_version: str = "0.0.0",
    outline_max_depth: int | None = None,
    ui_key: str | None = None,
) -> None:
    """
    Render a namespaced Streamlit manual viewer.

    This version supports multiple manual viewers on the same page by
    namespacing widget keys and session-state fields.
    """
    ns = _manual_ui_namespace(manual_rel_dir, ui_key=ui_key)
    state_keys = _manual_state_keys(ns)
    _init_manual_state(state_keys)

    manual_root = _prepare_manual_root(
        repo_root=repo_root,
        manual_rel_dir=manual_rel_dir,
        ensure_outline=ensure_outline,
        outline_title=outline_title,
        outline_version=outline_version,
        outline_max_depth=outline_max_depth,
    )
    if manual_root is None:
        return

    tree, flat = build_manual_index_cached(str(manual_root))
    if not flat:
        st.warning(f"No markdown files found under: {manual_root}")
        return

    with st.expander(expander_label, expanded=False):
        _render_manual_controls(ns=ns, state_keys=state_keys)

        with st.expander("Manual Map (Tree)", expanded=False):
            st.code(render_generated_tree_text(tree), language="text")

        _render_manual_search(ns=ns, flat=flat, state_keys=state_keys)
        _render_manual_sections(ns=ns, tree=tree, flat=flat, state_keys=state_keys)

    _render_manual_content(flat=flat, state_keys=state_keys, header_label="Manual")


def _render_folder_accordion(
    *,
    node,
    rel_prefix: Path,
    flat,
    expand_all: bool,
    selected_key: str,
    key_prefix: str,
) -> None:
    """
    Render nested manual folders/files with namespaced widget keys.
    """
    child_keys = sorted(node.keys(), key=numeric_sort_key)

    for name in child_keys:
        child = node[name]
        rel_path = rel_prefix / name

        if isinstance(child, dict):
            with st.expander(
                f"Folder: {name}",
                expanded=expand_all,
            ):
                _render_folder_accordion(
                    node=child,
                    rel_prefix=rel_path,
                    flat=flat,
                    expand_all=expand_all,
                    selected_key=selected_key,
                    key_prefix=f"{key_prefix}_{name}",
                )
            continue

        rel_str = rel_path.as_posix()
        mf = flat.get(rel_str)
        label = _format_section_label(mf, name)

        if st.session_state.get(selected_key) == rel_str:
            label = f"> {label}"

        if st.button(label, key=f"{key_prefix}_open_{rel_str}"):
            _toggle_selected(selected_key, rel_str)
