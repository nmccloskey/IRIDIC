# Manuals Policy

## 1. Purpose

This document defines standards for long-form manuals in IRIDIC-governed
repositories.

The goals are:

- keep public documentation modular and navigable
- make source-backed manual drafting traceable
- support human and LLM collaboration without losing review control
- allow manuals to grow without becoming monolithic
- keep authored, generated, and preparatory materials distinct

This page governs manual structure. The detailed drafting workflow,
object inventory process, itinerary system, review process, and export
workflow are defined in companion documents in this section.

------------------------------------------------------------------------

## 2. Manual Materials

IRIDIC distinguishes three kinds of manual-related material.

### Authored Manual

The authored manual is the public or near-public documentation tree.
It contains pages written for users, researchers, developers, or
maintainers.

Typical root:

    docs/manual/

### Generated Manual Views

Generated manual views are produced mechanically from code, tests,
example manifests, or other structured sources.

They may be composed with authored pages, but should not be hand-edited
unless the generator itself is being revised.

Example:

    src/package_name/examples/assets/rendered_docs/example_io/

### Manual Prep Workspace

The manual prep workspace is an internal drafting area used for
inventories, notes, file plans, itineraries, and review sweeps.

Typical root:

    .codex-local/manual_prep/

This area may be untracked. Its value is traceability: it allows the
human maintainer and an LLM assistant to work in Markdown files rather
than relying only on chat history.

------------------------------------------------------------------------

## 3. Authored Manual Root

The default authored manual root is:

    docs/manual/

A mature manual may use a numbered section layout:

    docs/manual/
      00_outline.md
      01_overview/
      02_operation/
      03_features/
      04_modules/
      05_functionalities/
      06_workflows/
      99_references.md

Not every repository needs every section. Small projects may begin with
only overview, operation, and selected module or command pages.

------------------------------------------------------------------------

## 4. Recommended Section Roles

### `00_outline.md`

The outline is the navigation map. It may be hand-authored or generated
from the manual tree.

It should reflect the current manual structure and be refreshed after
stable tree changes.

### `01_overview/`

Overview pages orient readers to the project, purpose, scope, audiences,
major functional areas, and manual organization.

Overview pages should not become command reference pages.

### `02_operation/`

Operation pages explain installation, command-line use, web-app use,
configuration, testing, and other general operating procedures.

These pages should cover repository-wide behavior that users need before
entering object-specific documentation.

### `03_features/`

Feature pages present especially important or cross-cutting concepts
early in the manual.

Features may overlap with modules, commands, functionalities, or
workflows. They receive feature status because they need prominent,
integrated explanation before lower-level details.

### `04_modules/`

Module pages describe cohesive operational domains.

Modules often contain command subdirectories.

### `05_functionalities/`

Functionality pages describe shared behavior that crosses multiple
modules or commands.

They prevent repeated explanations across command pages.

### `06_workflows/`

Workflow pages describe applied, multi-step procedures.

They should generally be drafted after relevant feature, module, command,
and functionality pages are stable enough to link outward.

### `99_references.md`

References collect citations, acknowledgments, and bibliographic support
for research-context pages.

------------------------------------------------------------------------

## 5. File Naming

Use numeric prefixes for stable ordering.

Top-level files and directories:

    NN_title.md
    NN_section_name/

Nested object and view files:

    04_modules/
      01_transcripts/
        01_quickstart.md
        03_research_context.md
        04_implementation_notes.md
        05_commands/
          01_tabularize/
            01_quickstart.md
            02_usage_guide.md
            04_implementation_notes.md

Guidelines:

- use lowercase filenames
- use underscores instead of spaces
- avoid special characters
- keep view numbers stable even when a view is absent
- avoid renumbering stable pages unless the manual structure truly
  changes

------------------------------------------------------------------------

## 6. Manual Page Size

Manual pages should be coherent and reasonably bounded.

As a rule of thumb:

- split a page once it becomes hard to review in one pass
- split when two audiences are being served by unrelated material
- split when one part changes frequently and another should remain stable
- avoid splitting solely for symmetry

The ontology should guide splits, but the practical question is whether
the file answers a distinct question.

------------------------------------------------------------------------

## 7. Internal Cross-References

Manuals should use references that survive later rendering choices.

If a project has no link-rewriting layer, relative Markdown links are
acceptable:

    See [Configuration](../02_operation/04_configuration.md).

If a project renders manual pages in an environment where Markdown links
may be misinterpreted, use plain path-bearing references:

    See Configuration (`docs/manual/02_operation/04_configuration.md`).

Choose one convention per repository and document it in the manual prep
overview or contribution notes.

------------------------------------------------------------------------

## 8. Source Grounding

Manual prose should be grounded in current repository behavior.

When sources conflict, use this precedence:

1. current source code and tests
2. generated examples and current run artifacts
3. current configuration defaults
4. current maintainer responses in prep files
5. older README or manual prose
6. archived drafts and chat history

Older documentation is useful as historical context, but it should not
override current source behavior.

------------------------------------------------------------------------

## 9. Prep Before Publication

Large manuals should not be drafted directly from a blank prompt into
public manual files.

A better workflow is:

1. create or refresh a manual prep workspace
2. ask the assistant to sweep the repository and produce an object
   inventory
3. let the maintainer respond inside that Markdown inventory
4. produce selection notes and a file plan
5. create smaller drafting itineraries
6. draft manual pages in serialized passes
7. run a human-review sweep
8. update outline, references, and export configuration

This keeps the process inspectable and prevents chat-only decisions from
becoming invisible.

------------------------------------------------------------------------

## 10. Export

Manual export to PDF or other publication formats is intentionally
separate from drafting policy.

The export stage should happen after the authored manual structure,
cross-references, references, and high-review items are stable.

See the manual export documentation for format-specific guidance.

------------------------------------------------------------------------

## 11. Summary

An IRIDIC manual is not only a folder of Markdown files. It is a
structured documentation system with authored pages, optional generated
views, and a traceable prep process.

The public manual should be clean and navigable. The prep workspace can
be messy, iterative, and richly annotated, because that is where the
human and assistant preserve the reasoning that makes the final manual
trustworthy.
