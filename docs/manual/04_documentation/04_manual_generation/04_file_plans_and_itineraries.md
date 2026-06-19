# File Plans And Drafting Itineraries

## 1. Purpose

File plans and itineraries convert an object inventory into manageable
manual drafting work.

The file plan says what the manual could contain.

The itineraries say how to draft it in orderly passes.

This distinction matters because large manuals are too complex to draft
well in one burst.

------------------------------------------------------------------------

## 2. File Plan

A file plan maps approved objects and views to target manual paths.

Recommended path:

    .codex-local/manual_prep/02_files/plans/file_plan_01.md

Use later pass numbers as needed:

    file_plan_02.md
    file_plan_03.md

------------------------------------------------------------------------

## 3. File Plan Columns

A useful file plan table includes:

| Column | Purpose |
| --- | --- |
| Path | Target authored manual path |
| Object Type | Feature, Module, Command, Functionality, Workflow |
| View Type | Quickstart, Usage Guide, Research Context, Implementation Notes, or integrated page |
| Purpose | One-sentence reason the file exists |
| Relevant Source Files | Code, tests, config, examples, or notes |
| Human Review | High, Medium, or Low |

The file plan should also list:

- intentionally deferred files
- generated views that stay outside authored manual pages
- objects that are covered elsewhere
- known source checks needed before drafting

------------------------------------------------------------------------

## 4. File Plan Boundaries

The file plan should not draft page contents.

It should be detailed enough that a future assistant can understand the
manual architecture, but not so detailed that every path adjustment
requires rewriting the whole plan.

When paths change during drafting, record the local path overlay in the
relevant itinerary. Consolidate stable changes into a later file plan
only when needed.

------------------------------------------------------------------------

## 5. Drafting Itineraries

Itineraries are pass-sized plans.

Recommended path:

    .codex-local/manual_prep/02_files/itineraries/

Recommended files:

    00_drafting_overview.md
    01_feature_draft_itinerary.md
    02_module_draft_itinerary.md
    03_command_draft_itinerary.md
    04_functionality_draft_itinerary.md
    05_workflow_draft_itinerary.md
    06_review_and_composition_itinerary.md

Itineraries make manual drafting resumable. A later assistant can read
the relevant itinerary and know what to do next.

------------------------------------------------------------------------

## 6. Drafting Overview

The drafting overview is the coordination file.

It should include:

- target authored manual root
- source documents to use
- current manual base
- cross-reference convention
- ground rules
- recommended path overlay
- drafting pass sequence
- page drafting pattern
- front matter or metadata recommendations
- review gates

This file should explain how the file plan maps onto the current manual
tree.

------------------------------------------------------------------------

## 7. Section Itineraries

Each section itinerary should include:

- purpose of the pass
- exact target tree
- current files to create, rename, or revise
- file plan segment with path overlay
- drafting order
- source files to inspect
- existing manual or prep material to consult
- content boundaries
- high-review flags
- cross-references to use
- drafting checklist
- out-of-scope work

This structure prevents an assistant from turning a planning pass into a
mass drafting pass.

------------------------------------------------------------------------

## 8. Recommended Drafting Order

Use this general order:

1. foundation pages
2. feature pages
3. module pages
4. command pages
5. functionality pages
6. workflow pages
7. review and composition

Rationale:

- foundation pages establish audience, operation, and terminology
- features explain concepts users need early
- modules establish domains before command detail
- command pages document user-invokable operations
- functionalities centralize repeated behavior after command needs are
  clearer
- workflows synthesize applied procedures after object-level pages exist

This order can be adjusted, but the reason for changing it should be
written down.

------------------------------------------------------------------------

## 9. Command Itinerary Pattern

Command drafting should usually happen by module.

For each module command pass:

1. read parent module pages
2. read command registry and dispatch logic
3. read implementation files
4. read relevant tests
5. skim generated examples
6. draft all Quickstarts
7. draft all Usage Guides
8. add Research Context only where non-redundant
9. draft Implementation Notes
10. check paths, syntax, config names, and output filenames

This keeps command terminology consistent while keeping each pass small
enough to verify.

------------------------------------------------------------------------

## 10. View-Specific Drafting

### Quickstart

Keep it short. Include the minimal action, minimal inputs, outputs, and
next step.

### Usage Guide

Explain ordinary operation, variants, input/output contracts, and common
pitfalls.

### Research Context

Use careful language. Add citations or review markers where claims carry
methodological weight.

### Implementation Notes

Ground the page in source files, execution flow, data flow, validation,
and failure modes useful for troubleshooting.

------------------------------------------------------------------------

## 11. Out-of-Scope Blocks

Every itinerary should state what is not in scope.

Examples:

- do not draft command pages in the module pass
- do not regenerate generated examples
- do not edit export configuration
- do not update references except for approved placeholders
- do not create workflow pages until object-level pages exist

Out-of-scope blocks are especially helpful in LLM-assisted work because
they keep the pass bounded.

------------------------------------------------------------------------

## 12. Verification

After each drafting pass, run checks appropriate to the change.

For documentation-only changes, checks may include:

- outline regeneration or inspection
- link/path search
- stale path search
- command syntax spot-checks against source
- generated-example path checks
- TODO search

Code tests are not always needed for prose-only changes, but if generated
examples, doctests, command docs, or docs-rendering scripts changed, run
the relevant tests.

------------------------------------------------------------------------

## 13. Itinerary Prompt

Use a prompt like this:

```text
Using the approved object inventory and file plan, create a drafting
itinerary for the next manual section.

Do not draft manual page contents yet.

Include the target tree, files to create or revise, source files to
inspect, dependencies on earlier pages, high-review flags, drafting
order, verification checks, and out-of-scope work.
```

------------------------------------------------------------------------

## 14. Summary

The file plan prevents the manual from drifting conceptually.

The itinerary prevents the drafting pass from drifting operationally.

Together, they let a human and assistant produce large manuals in
careful, reviewable pieces.
