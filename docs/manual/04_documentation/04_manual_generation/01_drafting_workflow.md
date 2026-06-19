# Manual Drafting Workflow

## 1. Purpose

This protocol defines a generalized workflow for using IRIDIC's manual
ontology to draft repository manuals with human and LLM collaboration.

The central lesson from applied manual drafting is that the assistant
should not move directly from repository scan to public manual pages.
The better workflow is to create a traceable Markdown preparation layer:
inventories, notes, file plans, itineraries, and review sweeps.

This makes the process reproducible, inspectable, and easier to resume
in later threads.

------------------------------------------------------------------------

## 2. Core Principle

Generate the manual in stages:

    repository sweep
      -> object inventory
      -> human responses
      -> object selection notes
      -> file plan
      -> drafting itineraries
      -> authored manual pages
      -> human-review sweep
      -> composition/export

Each stage produces Markdown artifacts that can be read by a human or an
assistant in a future session.

------------------------------------------------------------------------

## 3. Recommended Inputs

Before a major manual drafting pass, provide the assistant with:

- repository root
- current README
- existing manual or documentation folder
- `src/` tree
- CLI parser, command registry, or dispatch files
- web-app files, if present
- configuration defaults and example config files
- tests
- generated examples or example manifests
- relevant maintainer notes
- current IRIDIC documentation ontology and workflow pages

Older manual drafts can be included, but current source behavior should
override stale prose.

------------------------------------------------------------------------

## 4. Prep Workspace

Create a manual prep workspace before drafting at scale.

Recommended root:

    .codex-local/manual_prep/

Recommended structure:

    .codex-local/manual_prep/
      00_notes/
      01_objects/
      02_files/
        plans/
        itineraries/
      03_review/
      99_archive/

The prep workspace can be untracked. Its job is to preserve reasoning,
not to serve as public documentation.

See `05_manual_prep_workspace.md` for detailed conventions.

------------------------------------------------------------------------

## 5. Stage 1: Repository Sweep

Ask the assistant to inspect the repository and produce an object
inventory only.

The assistant should look for:

- modules and source-code domains
- CLI commands and web-app actions
- reusable cross-cutting functionality
- applied workflows
- early feature concepts
- generated documentation or example systems
- configuration and provenance behavior
- tests that reveal expected behavior

The assistant should not draft manual pages during this stage.

Output:

    .codex-local/manual_prep/01_objects/object_inventory_01.md

For later passes:

    object_inventory_02.md
    object_inventory_03.md

Use two-digit pass numbers for stable ordering.

------------------------------------------------------------------------

## 6. Stage 2: Human Response Loop

The object inventory should include questions, uncertainties, and
recommended documentation views.

The maintainer can respond directly in the Markdown file, adding a
`Human response` column or inline notes.

Useful response codes:

- `GQ`: good question; the maintainer shares the uncertainty and wants a
  conservative first draft with later review
- `PSC`: please see the code; the assistant should answer from source
  behavior during drafting and surface remaining ambiguity later

Human responses in a later inventory pass override earlier uncertainty
notes.

Output:

    .codex-local/manual_prep/01_objects/object_inventory_02.md
    .codex-local/manual_prep/01_objects/object_inventory_03.md
    .codex-local/manual_prep/01_objects/select_object_notes.md

See `06_object_inventory_sweeps.md` for details.

------------------------------------------------------------------------

## 7. Stage 3: File Plan

After the inventory is reviewed, produce a file plan.

The file plan maps selected objects and views to target authored manual
paths.

It should include:

- target path
- object type
- view type
- purpose
- relevant source files
- human review level
- intentionally deferred files
- generated views that should not be hand-authored

Output:

    .codex-local/manual_prep/02_files/plans/file_plan_01.md
    .codex-local/manual_prep/02_files/plans/file_plan_02.md

The file plan is a content plan, not a promise that every listed file
will be drafted immediately.

------------------------------------------------------------------------

## 8. Stage 4: Drafting Itineraries

Large file plans should be broken into smaller itineraries.

Itineraries convert the broad file plan into pass-sized drafting
instructions.

Recommended itinerary sequence:

    .codex-local/manual_prep/02_files/itineraries/
      00_drafting_overview.md
      01_feature_draft_itinerary.md
      02_module_draft_itinerary.md
      03_command_draft_itinerary.md
      04_functionality_draft_itinerary.md
      05_workflow_draft_itinerary.md
      06_review_and_composition_itinerary.md

Each itinerary should identify:

- target tree
- files to create or revise
- source files to inspect
- dependencies on earlier pages
- drafting order
- view policy
- high-review flags
- verification checks
- out-of-scope work

Use itineraries to handle path overlays when the file plan and current
manual tree diverge. Do not keep rewriting the file plan for every small
path adjustment.

See `07_file_plans_and_itineraries.md` for details.

------------------------------------------------------------------------

## 9. Stage 5: Draft Manual Pages

Draft manual pages in serialized passes.

Recommended order:

1. foundation pages
2. feature pages
3. module pages
4. command pages
5. functionality pages
6. workflow pages
7. composition, cross-references, references, and outline

This order lets early conceptual pages stabilize terminology before the
manual expands into many command and workflow pages.

For each small drafting pass:

1. read the itinerary segment
2. read the relevant inventory rows and human responses
3. read source files and tests named in the itinerary
4. read existing manual pages likely to be referenced
5. draft the target file or small file set
6. check command syntax, config names, filenames, and outputs against
   source
7. add `TODO:` only when a human decision remains or source behavior is
   ambiguous
8. report what changed and what remains uncertain

------------------------------------------------------------------------

## 10. Stage 6: Human-Review Sweep

After a section or major pass is drafted, run a human-review sweep.

The assistant should inspect drafted pages and collect review needs in
dedicated review itinerary files.

Recommended root:

    .codex-local/manual_prep/03_review/

Example files:

    human_review_itinerary_section_01.md
    human_review_itinerary_section_03.md
    human_review_itinerary_section_05.md

Review items should have stable IDs:

    HR-03-001
    HR-05-014

Each item should include:

- file path
- problem area
- concern
- suggested action
- human response
- follow-up

See `08_human_review_sweeps.md` for details.

------------------------------------------------------------------------

## 11. Stage 7: Composition and Export

Only after drafting and review should the maintainer update final
composition artifacts:

- outline
- references
- cross-reference conventions
- generated-view composition
- export configuration

Export details are handled separately. Do not let PDF or web rendering
requirements drive early content drafting unless they affect file
structure.

------------------------------------------------------------------------

## 12. Ground Rules

Use these rules throughout the workflow:

- Source code overrides old manual prose, README prose, stale notes, and
  chat memory.
- Human responses in the latest prep file override earlier assistant
  uncertainty notes.
- Generated views should remain generated.
- Do not create a view file unless it answers a non-redundant question.
- Preserve `TODO:` markers for real unresolved human-review items.
- Treat methodological, privacy, validation, and workflow-order claims
  as high-review content.
- Prefer smaller serialized drafting passes over mass file generation.
- Keep prep artifacts readable enough that a future assistant can resume
  from them.

------------------------------------------------------------------------

## 13. Starter Prompt

Use a prompt like this to begin a new repository manual pass:

```text
Please use the IRIDIC manual ontology and drafting workflow.

First, do not draft manual pages. Sweep this repository and create a
documentation object inventory in Markdown.

Classify likely documentation targets as Feature, Module, Command,
Functionality, or Workflow. For each object, include relevant source
files, user-facing commands or actions, recommended views, uncertainties
for human review, and likely review priority.

Use current source behavior over older README or manual prose. Mark
questions that require human judgment clearly.
```

After the maintainer responds to the inventory, use follow-up prompts for
selection notes, file planning, itinerary planning, drafting, and review
sweeps.

------------------------------------------------------------------------

## 14. Applied Pattern From DIAAD

This workflow was generalized from the DIAAD manual drafting process.

The useful pattern was not project-specific terminology, but the
artifact sequence:

- a local `manual_prep` workspace for traceable Markdown collaboration
- `00_notes/` for human-supplied methodological and workflow context
- repeated object inventories that incorporated source sweeps and human
  responses
- selection notes that converted the inventory into planning decisions
- a file plan that mapped objects and views to authored manual paths
- section itineraries that serialized drafting by features, modules,
  commands, functionalities, and workflows
- human-review itineraries that swept drafted pages for claims requiring
  maintainer judgment

When applying this workflow to another repository, replace DIAAD's
domain objects with that repository's objects, but preserve the staging
logic. The goal is for a future assistant to understand the framework by
reading the prep artifacts, not by reconstructing decisions from chat
history.

------------------------------------------------------------------------

## 15. Summary

The IRIDIC manual drafting workflow turns LLM assistance into a
traceable documentation process.

The assistant sweeps and proposes. The human responds and prioritizes.
The file plan and itineraries serialize the work. Drafts remain grounded
in source behavior. Review sweeps make uncertainty visible before the
manual becomes authoritative.
