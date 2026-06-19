# Human Review Sweeps

## 1. Purpose

A human-review sweep identifies claims, instructions, and uncertainties
that need maintainer inspection before publication.

The sweep is not the same as proofreading. It is a structured review of
risk.

It asks:

- What could mislead a user?
- What needs source re-checking?
- What needs methodological review?
- What needs privacy or deployment review?
- What TODO markers should be resolved, retained, or centralized?

------------------------------------------------------------------------

## 2. When To Run A Sweep

Run a review sweep after:

- a section is drafted
- a feature or module pass is complete
- many command pages have been added
- workflow pages start making sequencing recommendations
- generated examples or config defaults have changed
- the manual is approaching release

For large manuals, run section-level sweeps rather than waiting until the
end.

------------------------------------------------------------------------

## 3. Recommended Location

Store review artifacts under:

    .codex-local/manual_prep/03_review/

Example:

    human_review_itinerary_section_01.md
    human_review_itinerary_section_03.md
    human_review_itinerary_section_05.md

The review files are prep artifacts. They do not need to be public manual
pages.

------------------------------------------------------------------------

## 4. Review Item Format

Use stable review IDs:

    HR-03-001
    HR-03-002

Recommended item shape:

```md
### HR-03-001 - Short Review Title

- Problem area: `Section or heading name`.
- Concern: Explain what needs review and why it matters.
- Suggested action: Describe what the maintainer should check or decide.
- Human response:
- Follow-up:
```

Group items by file.

```md
## File: `docs/manual/03_features/01_transcript_tabularization.md`
```

------------------------------------------------------------------------

## 5. Review Priority

Use review priority to focus attention.

### High Review

High-review items can affect interpretation, ethics, validity, privacy,
or major workflow decisions.

Examples:

- privacy and de-identification claims
- hosted web-app safety language
- blinding and unblinding recommendations
- reliability thresholds
- validation claims
- methodological claims
- workflow-order recommendations
- output interpretation

### Medium Review

Medium-review items are operationally important and should be checked
against source behavior.

Examples:

- command syntax
- config defaults
- output filenames
- workbook sheet names
- web-app action availability
- generated example package layout

### Low Review

Low-review items are mostly navigational or maintenance-oriented.

Examples:

- outline wording
- cross-reference style
- source-verified command summaries
- generated-doc composition notes

------------------------------------------------------------------------

## 6. Sweep Procedure

For each section:

1. read every drafted page
2. search for `TODO:`, `Draft Review Notes`, and known review markers
3. compare high-impact claims against source, tests, config, or notes
4. record unresolved concerns as review items
5. make small source-backed corrections only when they are clearly safe
6. record corrections in a `Resolved During This Sweep` section

Do not silently resolve methodological or policy questions. Put them in
the review file.

------------------------------------------------------------------------

## 7. Source-Backed Edits During Review

The assistant may make small corrections during a sweep when:

- the source clearly resolves the issue
- the edit is narrow
- no human judgment is required
- the change does not alter policy or interpretation

Examples:

- fixing a stale file path
- correcting a command name from the current registry
- updating a renamed page reference
- replacing an old config field name after source verification

Record these under:

```md
## Resolved During This Sweep

- Updated stale Read Next reference from ...
- Corrected command name ...
```

------------------------------------------------------------------------

## 8. TODO Markers

TODO markers inside manual pages are useful during drafting but can
become scattered.

The review sweep should:

- find all TODOs
- decide whether each should stay in the manual page
- move broader review needs into the review itinerary
- remove TODOs that are resolved
- preserve TODOs that intentionally signal unpublished uncertainty

For publication-facing pages, prefer resolved prose unless the manual is
explicitly being released with known open questions.

------------------------------------------------------------------------

## 9. Human Response Loop

The maintainer can respond directly in review files.

Possible responses:

- approve current wording
- request a rewrite
- provide corrected wording
- mark for source verification
- defer until references are finalized
- decide that a claim should be removed

After response, a follow-up pass should update the authored manual pages
and mark the review item resolved or still open.

------------------------------------------------------------------------

## 10. Review Sweep Prompt

Use a prompt like this:

```text
Please run an IRIDIC-style human-review sweep for this manual section.

Read the drafted pages and create a review itinerary in
.codex-local/manual_prep/03_review/.

Identify high-review, medium-review, and low-review concerns. Include
file paths, problem areas, concerns, suggested actions, and blank fields
for human response and follow-up.

Make only narrow source-backed corrections during the sweep. Record any
such corrections under "Resolved During This Sweep."
```

------------------------------------------------------------------------

## 11. Release Gate

Before publication or release, review:

- all high-review items
- all TODO markers
- command syntax and config defaults
- generated example references
- privacy and data-governance language
- references and citations
- workflow sequencing claims

The manual does not need to be perfect, but known uncertainty should be
visible and intentional.

------------------------------------------------------------------------

## 12. Summary

Human-review sweeps turn scattered uncertainty into a structured review
queue.

They are especially important for research software manuals, where a
wrong sentence can affect analysis choices, privacy decisions, or the
interpretation of results.
