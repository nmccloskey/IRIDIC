# Manual Prep Workspace

## 1. Purpose

The manual prep workspace is the staging area for LLM-assisted manual
drafting.

It exists because large manuals are easier to build when decisions are
captured in Markdown files rather than scattered across chat turns.

The prep workspace lets a human maintainer and an assistant:

- preserve repository-sweep results
- answer documentation questions inline
- add domain notes and methodological context
- plan files before drafting them
- serialize drafting into manageable passes
- track high-review claims before publication

------------------------------------------------------------------------

## 2. Recommended Location

Use a repository-local, non-public workspace:

    .codex-local/manual_prep/

This folder may be untracked. If it contains sensitive notes, draft
research prose, or internal review comments, keep it out of normal
distribution artifacts.

Projects may use another location, but the path should be explicit in
the drafting prompt.

------------------------------------------------------------------------

## 3. Recommended Structure

Use this structure for substantial manuals:

    .codex-local/manual_prep/
      00_notes/
      01_objects/
      02_files/
        plans/
        itineraries/
      03_review/
      99_archive/

The numeric prefixes keep the workflow readable:

- notes before inventories
- inventories before file plans
- plans before itineraries
- review after drafting
- archives at the end

------------------------------------------------------------------------

## 4. `00_notes/`

Use `00_notes/` for human-provided context that should inform manual
drafting.

Examples:

- research-method notes
- excerpts from a paper draft
- lab workflow descriptions
- module-specific conceptual notes
- privacy or deployment cautions
- validation or citation notes

Notes are source material, not final manual prose. The assistant should
synthesize them with source behavior and should not copy them blindly
into public documentation.

Good note files are specific enough to be useful later:

    00_notes/
      00_drafting_notes.md
      01_project_writeup_excerpts.md
      02_domain_method_notes.md
      03_workflow_notes.md

------------------------------------------------------------------------

## 5. `01_objects/`

Use `01_objects/` for object inventories and selection notes.

Example:

    01_objects/
      object_inventory_01.md
      object_inventory_02.md
      object_inventory_03.md
      select_object_notes.md
      archive/

Object inventories should record what the assistant found during a
repository sweep.

Later inventory passes should incorporate:

- code changes
- maintainer responses
- corrected object classifications
- new or removed commands
- newly discovered generated views

Selection notes convert the inventory into planning decisions.

------------------------------------------------------------------------

## 6. `02_files/plans/`

Use `02_files/plans/` for broad manual file plans.

Example:

    02_files/
      plans/
        file_plan_01.md
        file_plan_02.md

A file plan maps objects and views to authored manual paths.

It should include:

- target file path
- object type
- view type
- one-sentence purpose
- relevant source files
- human review priority
- deferred files
- generated files that should not be hand-authored

The file plan is intentionally broader than a single drafting pass.

------------------------------------------------------------------------

## 7. `02_files/itineraries/`

Use `02_files/itineraries/` for pass-sized drafting plans.

Example:

    02_files/
      itineraries/
        00_drafting_overview.md
        01_feature_draft_itinerary.md
        02_module_draft_itinerary.md
        03_command_draft_itinerary.md
        04_functionality_draft_itinerary.md
        05_workflow_draft_itinerary.md

Itineraries are especially useful when:

- the file plan is large
- paths have changed since the file plan was written
- source files must be inspected before drafting
- high-review content needs to be preserved
- command families should be drafted one module at a time

An itinerary should say what to draft next and what not to draft yet.

------------------------------------------------------------------------

## 8. `03_review/`

Use `03_review/` for review sweeps after drafting.

Example:

    03_review/
      human_review_itinerary_section_01.md
      human_review_itinerary_section_03.md
      human_review_itinerary_section_05.md

Review files should collect concerns in stable, addressable items.

They are useful because `TODO:` markers in many manual pages can become
hard to manage once the manual grows.

------------------------------------------------------------------------

## 9. `99_archive/`

Use `99_archive/` for old inventories, obsolete manual drafts, and
snapshots that should be preserved but not used as current authority.

Archived files can seed future prose, but source code and current prep
artifacts should override them.

------------------------------------------------------------------------

## 10. Naming Conventions

Use two-digit pass numbers:

    object_inventory_01.md
    object_inventory_02.md
    file_plan_01.md
    file_plan_02.md

Use explicit section names for itineraries:

    03_command_draft_itinerary.md
    04_functionality_draft_itinerary.md

Use stable review IDs:

    HR-03-001
    HR-03-002

The goal is to make artifacts easy to cite in later prompts.

------------------------------------------------------------------------

## 11. Prompt Handoff

When resuming work in a new thread, provide the assistant with:

- this IRIDIC documentation section
- the repository root
- the latest object inventory
- selection notes
- the latest file plan
- the relevant drafting itinerary
- any notes needed for the current section
- review files if the task is cleanup or revision

This gives the assistant a solid framework without requiring the whole
chat history.

------------------------------------------------------------------------

## 12. Summary

The manual prep workspace is deliberately practical.

It lets a project preserve the useful parts of LLM collaboration:
repository sweeps, questions, human responses, source maps, file plans,
drafting order, and review concerns.

The final manual should be polished. The prep workspace should be
honest, traceable, and easy to resume.
