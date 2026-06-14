# IRIDIC Protocol: AI-Assisted Example I/O Module Development

## Overview

This protocol describes a repeatable workflow for using an AI assistant to build
or expand an Example I/O module in an IRIDIC-compliant repository. It abstracts
from the DIAAD Example I/O development workflow, where iterative no-edit design
passes, serialized implementation passes, generated documentation, downloadable
example packages, and manual-composition handoff notes were developed together.

The goal is to help both the developer and the AI assistant work deliberately:
clarify the documentation architecture before coding, preserve single sources of
truth, keep generated files auditable, and leave behind enough local planning
material that future passes or adjacent repositories can continue smoothly.

This protocol complements `05_example_io/01_policy.md`. The policy defines what
Example I/O should be; this protocol defines how to build it with AI assistance.

## Core Principles

### 1. Start With Design, Not Edits

Begin with no-edit design passes when the Example I/O layer touches multiple
concerns, such as CLI behavior, webapp behavior, generated documentation,
manual composition, downloadable file packages, or adjacent tools.

A no-edit pass should:

- name the immediate user need;
- identify relevant existing code, docs, and policies;
- surface tensions in the design;
- propose a staged implementation path;
- clarify vocabulary and object identity;
- defer file edits until the developer agrees on the direction.

This is especially important when the assistant is synthesizing across parallel
workflows, such as a software feature, a documentation ontology, and a future
manual builder.

### 2. Serialize Work Into Passes

Plan the work as a sequence of passes rather than as one broad coding request.
Each pass should have a clear purpose, scope, verification plan, and risk note.

A useful pass plan includes:

- pass name;
- minimum anticipated reasoning level;
- purpose;
- scope;
- why this pass belongs in this order;
- verification steps;
- risks or likely follow-up passes.

The developer and assistant should prefer pass parsimony: use the smallest
number of passes that keeps the assistant from mixing unrelated types of work.
For example, do not combine front-matter identity work with a broad path-render
rewrite if both can be validated separately.

### 3. Keep A Local Itinerary

Maintain a local planning file, often outside tracked source files, for the
Example I/O workflow. In DIAAD, this was done in a file like:

```text
.codex-local/itineraries/example_module_commands.md
```

The itinerary should record:

- baseline state;
- design principles;
- stable identifiers;
- SSOT layers;
- desired user-facing shape;
- pass sequence;
- verification expectations;
- known risks.

When the plan changes substantially, archive the previous version rather than
overwriting its history. For example:

```text
.codex-local/itineraries/archive/example_module_commands_YYMMDD_HHMM.md
```

The archive is not bureaucracy. It preserves the reasoning trail when a later
pass discovers that the ontology, package structure, or integration target has
shifted.

### 4. Give The Assistant Policy Context

Before implementation, provide the assistant with the relevant documentation and
software policies. These may include:

- Example I/O policy;
- documentation ontology;
- documentation generation protocol;
- CLI or webapp command policy;
- testing policy;
- manual composition notes;
- prior chat notes that define vocabulary or architectural choices.

The assistant should not have to infer long-range goals only from code. A short
policy packet can prevent local changes from conflicting with the broader IRIDIC
manual architecture.

### 5. Use Handoff Notes For Adjacent Systems

When the Example I/O work creates future obligations for another repository or
subsystem, create handoff notes during the originating workflow.

A handoff note should explain:

- what was implemented in the current repository;
- which metadata or helper boundaries matter;
- which assumptions the adjacent system should preserve;
- which files or generated artifacts are examples rather than authoritative
  source;
- which regression checks are worth generalizing.

For DIAAD, this took the form of a note like:

```text
.codex-local/itineraries/DIAAD_oriented_PSAIR_notes_for_user_example_manual_synthesis.md
```

The general lesson is: do not make the next repository rediscover the design
from diffs.

## Recommended Workflow

### Phase 1: Orientation And Inventory

Ask the assistant to inspect the repository before proposing implementation.
The assistant should identify:

- existing command registries;
- current example assets;
- current generated docs;
- existing tests;
- webapp or CLI entry points;
- config conventions;
- documentation roots;
- generated-file conventions;
- ignored or local-only planning directories.

The output of this phase should be a concise summary of the current shape and
any obvious mismatches with the Example I/O policy.

### Phase 2: No-Edit Design Passes

Use one or more no-edit passes to settle the architecture.

Common design questions include:

- Is the full example dataset a normal command, an omnibus command, a workflow,
  or a collection object?
- Are command-specific examples generated from the same artifacts as the full
  dataset?
- What is the stable object identifier: `command_id`, `workflow_id`, module ID,
  or something else?
- Should generated command docs display package atlas paths or normal runtime
  paths?
- How will authored manual pages and generated Example I/O pages compose later?
- What should be tracked, generated, ignored, or downloaded?

The assistant should be encouraged to identify design tensions explicitly. For
example, a full example dataset may be useful as an atlas even though command
pages should show runtime-shaped output paths.

### Phase 3: Pass Itinerary

Ask the assistant to write or update the itinerary file before coding begins.

A robust itinerary usually separates these concerns:

1. command identity and front matter;
2. artifact and path registry;
3. package generation and manifests;
4. webapp or CLI integration;
5. manual-composition contract;
6. cleanup and duplication reduction.

The exact order depends on the repository, but identity should usually precede
path rewrites and manifest generation. Once object identity is stable, tests can
assert relationships by ID instead of by fragile paths.

### Phase 4: Implementation Passes

For each implementation pass, the assistant should:

- restate the current pass scope;
- read the relevant files;
- make narrowly scoped edits;
- preserve existing code style and local helpers;
- avoid broad refactors unless the pass is explicitly a cleanup pass;
- update tests in proportion to risk;
- run the repository's documented test commands;
- report warnings, failures, and residual risks.

The developer should review each pass outcome before starting the next pass,
especially when the next pass depends on terminology or metadata introduced by
the previous one.

### Phase 5: Generated Documentation And Packages

When generating Example I/O docs or downloadable file packages, preserve a clear
separation between:

- source specifications;
- generated example assets;
- rendered markdown;
- package manifests;
- user-facing runtime paths;
- full-dataset atlas paths.

A useful pattern is to represent the same artifact in multiple contexts:

```text
runtime_display_path:
  diaad_data/output/diaad_YYMMDD_HHMM/cu_coding/cu_coding.xlsx

command_package_path:
  example_output/cu_coding/cu_coding.xlsx

full_dataset_atlas_path:
  expected_outputs/cus_module/cus_files/cu_coding.xlsx
```

The command-specific Example I/O page should usually show the runtime path. The
full-dataset README or manifest can document the atlas path.

### Phase 6: Manual Composition Contract

Generated Example I/O pages should include front matter that allows a manual
composer to slot them beside authored pages without path-specific logic.

Recommended fields include:

```yaml
object_type: command
object_types:
  - command
object_id: transcripts.tabularize
command_id: transcripts.tabularize
canonical_command: transcripts tabularize
module_id: transcripts
view: example_io
view_label: Example I/O
view_order: 50
slot: examples
source_manual: generated_example_io
generated: true
title: Transcript Tabularization Example
```

For full-dataset or omnibus pages, use the appropriate primary object type and
stable workflow identity:

```yaml
object_type: workflow
object_types:
  - workflow
  - command
object_id: full_example_dataset
workflow_id: full_example_dataset
command_id: examples
command_subtype: omnibus
view: example_io
```

The manual composer should group pages by `object_type + object_id` and then
render views by `view_order` or a project-defined view order.

### Phase 7: Handoff And Cleanup

After the main behavior works, complete a cleanup pass. This pass should reduce
obvious duplication while preserving useful command-specific prose.

Good cleanup targets include:

- command-to-doc builder registries;
- command-to-output-path helper functions;
- shared front-matter helper functions;
- manifest rendering helpers;
- tests that assert registry coverage.

Avoid over-templating. A generated Example I/O system should be structurally
consistent, but individual command pages may still need command-specific notes.

## Suggested Pass Pattern

A generalized pass sequence is:

### Pass 1: Baseline And Output Destination

Clarify where generated examples should be written, how logs are created, and
whether the Example I/O generator follows the normal run context.

### Pass 2: Package Shape And Cleanup

Settle full-dataset versus command-specific package layouts. Remove obsolete
options or misleading folders. Ensure temporary scratch artifacts are not left in
user-facing output.

### Pass 3: Command Selection Interface

Add command-specific example selection, such as `--for-command`, and ensure the
webapp can request examples for selected functions.

### Pass 4: Command Coverage

Expand example generation across command groups. Use sub-passes if coverage is
large. Validate shared input capabilities and command sequencing.

### Pass 5: Webapp And Download Experience

Expose example downloads in the user interface without treating the examples
command as an ordinary analysis command.

### Pass 6: Documentation Identity

Introduce stable IDs, rendered doc paths, and front matter.

### Pass 7: Artifact Registry And Runtime Paths

Replace hardcoded output paths with artifact/path helpers. Show runtime-shaped
paths in command pages and atlas paths only where appropriate.

### Pass 8: Manifests And README Notes

Generate machine-readable manifests and explain full-dataset atlas layouts.

### Pass 9: Manual Composition Contract

Document how generated Example I/O views compose with authored manual views.
Prepare handoff notes for any adjacent system.

### Pass 10: Renderer Cleanup

Consolidate helpers and registries after behavior has settled.

This sequence is a template, not a requirement. Repositories with simpler
Example I/O needs may combine passes, but should still preserve the order of
reasoning: identity before rendering, rendering before manifests, manifests
before cleanup.

## Roles And Responsibilities

### Developer Responsibilities

The developer should:

- provide policy context and integration goals;
- decide when a no-edit design pass is needed;
- approve the pass sequence;
- clarify terminology and object identity;
- review warnings and residual risks;
- archive important itinerary revisions.

### AI Assistant Responsibilities

The assistant should:

- read local policy and code before editing;
- maintain a current understanding of the itinerary;
- make scoped changes per pass;
- avoid reverting user changes;
- preserve SSOT boundaries;
- add targeted tests;
- run the documented test commands;
- explicitly report issues, warnings, and skipped checks;
- update handoff notes when the work affects adjacent systems.

## Verification Expectations

A mature Example I/O workflow should test:

- every supported command has an example plan;
- every example plan has a rendered Example I/O page;
- every generated command page has valid front matter;
- generated command pages use runtime-shaped paths;
- full-dataset package manifests document atlas paths;
- every manifest artifact path exists;
- command-specific packages do not contain full-dataset-only folders unless
  intentionally documented;
- webapp and CLI entry points expose examples in the intended way;
- generated docs can be regenerated deterministically enough for review.

For AI-assisted work, test output should be reported concretely. Do not claim
success unless the repository's actual test runner completed successfully.
Warnings should be reported even when tests pass.

## Common Pitfalls

### Pitfall: Starting With A Broad Rewrite

Avoid asking the assistant to build the whole Example I/O system in one pass.
This tends to mix ontology, rendering, package layout, and UI behavior.

### Pitfall: Treating Generated Markdown As SSOT

Generated markdown is an output. Update specs, renderers, helpers, or generated
artifacts instead.

### Pitfall: Encoding Physical Paths As Identity

Use stable IDs such as `command_id` and `workflow_id`. Numeric prefixes and file
paths are useful for navigation, not identity.

### Pitfall: Hiding Full-Dataset Atlas Paths In Command Docs

Command-specific docs should usually show what a user sees after running the
command. Full-dataset atlas paths belong in full-dataset manifests, READMEs, or
overview pages.

### Pitfall: Skipping Handoff Notes

If the Example I/O work affects a manual composer, webapp, package builder, or
another repository, write down the interface while it is fresh.

## Local Planning Artifacts

A repository may use untracked or locally tracked planning artifacts such as:

```text
.codex-local/itineraries/example_module_commands.md
.codex-local/itineraries/archive/example_module_commands_YYMMDD_HHMM.md
.codex-local/chats/manual_framework_notes.md
.codex-local/itineraries/<repo>_handoff_notes.md
```

These files are working memory for the developer and AI assistant. They should
be concise enough to guide future work, but detailed enough to preserve the
reasoning behind the architecture.

## Summary

An AI-assisted Example I/O build works best when the assistant is treated as a
collaborator in staged design, not just a code generator. The durable pattern is:

1. orient to existing code and policy;
2. run no-edit design passes;
3. write a pass itinerary;
4. implement one concern at a time;
5. verify with repository-specific tests;
6. preserve SSOT boundaries;
7. leave handoff notes for adjacent systems.

This approach produces Example I/O modules that are easier to extend, easier to
compose into manuals, and less likely to drift away from the software behavior
they are meant to document.
