# Object Inventory Sweeps

## 1. Purpose

An object inventory sweep is the first major step in IRIDIC-style manual
generation.

The assistant inspects the repository and proposes documentation
objects. It does not draft user manual pages yet.

The inventory answers:

- What needs documentation?
- What object type is each target?
- What source files define or constrain it?
- What views are likely useful?
- What questions require human review?

------------------------------------------------------------------------

## 2. When To Run A Sweep

Run an object inventory sweep when:

- creating a new manual
- replacing an obsolete manual
- major CLI or web-app behavior has changed
- generated examples or configuration behavior has changed
- the maintainer wants to re-plan documentation before drafting

For fast updates to a small section, a full inventory may be unnecessary.
For a large manual, it is worth the time.

------------------------------------------------------------------------

## 3. Sources To Inspect

The assistant should inspect, when present:

- `README.md`
- `pyproject.toml`
- `src/`
- CLI command registries
- parser and dispatch files
- web-app files
- configuration defaults
- example configuration files
- generated examples and manifests
- tests
- existing manual pages
- local command notes
- manual prep notes
- archived manual drafts

Current source behavior should override older prose.

------------------------------------------------------------------------

## 4. Inventory Table

A useful inventory table includes:

| Column | Purpose |
| --- | --- |
| Proposed object name | Human-readable name |
| Object type | Feature, Module, Command, Functionality, or Workflow |
| Relevant source files | Code, tests, config, examples, or notes to inspect |
| User-facing commands or actions | CLI commands, web actions, or entry points |
| Recommended views | QS, UG, RC, IN, generated views |
| Uncertainties or questions | Items needing source check or human judgment |
| Human response | Maintainer answer, correction, or review note |

Shorthand may be used:

- `QS`: Quickstart
- `UG`: Usage Guide
- `RC`: Research Context
- `IN`: Implementation Notes

------------------------------------------------------------------------

## 5. Material Updates

Each later inventory pass should begin with a short material-updates
section.

This section should list changes since the previous pass, such as:

- new commands
- removed command flags
- updated config behavior
- changed generated-example layout
- new web-app actions
- stricter file discovery
- new tests that clarify behavior
- archived manual prose that is now stale

This prevents later planning from resting on obsolete assumptions.

------------------------------------------------------------------------

## 6. Human Responses

The maintainer should respond directly in the inventory file where
possible.

Human responses may:

- approve an object
- reject or merge an object
- reclassify an object
- clarify terminology
- add methodological context
- mark an issue for later review
- tell the assistant to check the code during drafting

Two useful response codes are:

- `GQ`: good question; draft conservatively and keep a review flag
- `PSC`: please see the code; source behavior should answer the question
  during drafting

These codes are not magic. They are compact conventions for preserving
human intent.

------------------------------------------------------------------------

## 7. Selection Notes

After the inventory has human responses, create selection notes.

Recommended path:

    .codex-local/manual_prep/01_objects/select_object_notes.md

Selection notes should record:

- objects selected for current planning
- objects deferred
- objects rejected or merged
- dual classifications
- feature/functionality boundaries
- module order
- command coverage
- workflow deferrals
- high-review topics

Selection notes bridge the inventory and the file plan.

------------------------------------------------------------------------

## 8. Generated Views

If a repository has generated documentation views, record them in the
inventory.

Generated views should include:

- where the generated files live
- whether they are user-facing or maintainer-facing
- how they are keyed to objects
- whether they should compose with authored pages
- whether they should be excluded from hand-authored manual trees

Generated views should not be copied into authored files just to make
the manual look complete.

------------------------------------------------------------------------

## 9. Inventory Prompt

Use a prompt like this:

```text
Please inspect this repository and produce an IRIDIC-style documentation
object inventory. Do not draft manual files yet.

Classify likely documentation targets as:
- Feature
- Module
- Command
- Functionality
- Workflow

For each object, include:
- proposed object name
- object type
- relevant source files
- relevant CLI commands or web-app actions
- recommended documentation views
- uncertainties or questions for human review
- likely review priority

Use current source behavior over older README or manual prose. Note any
generated documentation views separately.
```

------------------------------------------------------------------------

## 10. Assistant Rules

During an inventory sweep, the assistant should:

- inspect source before classifying command behavior
- distinguish current behavior from planned behavior
- mark uncertainty instead of guessing
- avoid drafting manual prose
- avoid over-fitting the manual to one old draft
- identify high-review claims early
- preserve source paths for later drafting

------------------------------------------------------------------------

## 11. Summary

The object inventory is the documentation equivalent of a field survey.

It gives the human maintainer a structured way to correct, enrich, and
prioritize the assistant's understanding before any public manual pages
are created.
