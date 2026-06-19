# Manual Ontology Policy

## 1. Purpose

This document defines the IRIDIC ontology for repository manuals.

The ontology separates:

- **objects**: what is being documented
- **views**: how that object is explained

This separation supports:

- modular user manuals
- source-backed documentation generation
- human review of high-risk claims
- LLM-assisted drafting
- generated views that can compose with authored pages

The ontology is a drafting tool, not a rigid filing mandate. A page
should exist only when it answers a distinct, useful question.

------------------------------------------------------------------------

## 2. Documentation Objects

Objects are documentation targets.

### Feature

A feature is an important or cross-cutting concept that deserves
prominent treatment early in the manual.

Features may overlap with lower-level objects.

Examples:

- transcript tabularization as a central data-model concept
- exact file name matching as a reproducibility safeguard
- generated example I/O as a documentation-composition concept
- word counting versus target vocabulary coverage as a methodological
  distinction spanning multiple modules

Use features when users need conceptual orientation before entering
module, command, functionality, or workflow pages.

### Module

A module is a cohesive operational domain.

Examples:

- transcripts
- templates
- word counting
- blinding

Modules often group several commands that operate on shared data
structures or serve a common workflow area.

### Command

A command is a discrete user-invokable operation.

Commands may be CLI commands, web-app actions, or other explicit user
operations.

Examples:

- `transcripts tabularize`
- `words analyze`
- `blinding encode`
- `examples`

Commands are the primary unit for operational instructions.

### Functionality

A functionality is reusable behavior that appears across multiple
modules, commands, or workflows.

Examples:

- configuration sources and overrides
- run provenance
- blinding and unblinding
- reliability selection and reselection
- speaking-time rate calculation

Functionality pages prevent repeated explanations across command pages.

### Workflow

A workflow is an applied multi-step procedure.

Examples:

- first local CLI run
- transcription reliability workflow
- monologic narrative analysis workflow
- web-app example-package workflow

Workflow pages should guide sequencing, decision points, and checks.
They should link outward to command and functionality pages rather than
reprinting every command reference.

------------------------------------------------------------------------

## 3. Dual Classification

Some documentation targets legitimately belong to more than one object
type.

Examples:

- blinding may be both a module and a cross-cutting functionality
- an examples system may be a module, a command, and a workflow-like
  collection
- transcript tabularization may be both a command and a feature

Dual classification is acceptable when each object view answers a
different question.

Avoid duplicating content. Use the more general page for conceptual
framing and the more specific page for operational detail.

------------------------------------------------------------------------

## 4. Documentation Views

Views define the explanatory stance of a page.

### Quickstart

Guiding question:

> What do I do first?

Use for brief, action-oriented orientation.

Common contents:

- one- to three-sentence purpose
- minimal command or action
- required inputs
- primary outputs
- immediate next step
- links or references to deeper pages

### Usage Guide

Guiding question:

> How do I use this correctly in ordinary work?

Use for operational detail.

Common contents:

- expected file layout
- command variants and flags
- important configuration settings
- input and output contracts
- common mistakes
- inspection or editing steps
- recovery paths

### Research Context

Guiding question:

> Why does this matter methodologically?

Use for research rationale, interpretation, cautions, and limits.

Common contents:

- role in research workflows
- methodological rationale
- interpretation boundaries
- relevant citations
- validity or reliability cautions
- TODO markers for claims needing review

### Implementation Notes

Guiding question:

> How does this work under the hood?

Use for technical transparency.

Common contents:

- source files
- dispatch or execution flow
- key functions or classes
- data flow
- validation and discovery behavior
- failure modes
- extension points

Implementation Notes should be useful for troubleshooting and
maintenance, but they should not narrate every helper function.

### Generated or Composable Views

Some views are generated from structured sources rather than authored
directly.

Example:

    example_io

Generated views may be composed with authored views through metadata,
front matter, object IDs, command IDs, or another composition layer.

Generated views are not replacements for authored Quickstart, Usage
Guide, Research Context, or Implementation Notes pages. They answer a
different question: what does the example, run artifact, or structured
output show?

------------------------------------------------------------------------

## 5. View Matrix

Use this matrix as a starting point.

| Object type | Quickstart | Usage Guide | Research Context | Implementation Notes |
| --- | --- | --- | --- | --- |
| Feature | Integrated | Optional | Optional | Optional |
| Module | Required | Optional | Required | Required |
| Command | Required | Required | Optional | Required |
| Functionality | Usually | Usually | Usually | Optional/Usually |
| Workflow | Required | Required | Light/Required | Optional |

Interpretation:

- Features often work best as integrated pages rather than split view
  files.
- Modules usually need conceptual framing and architecture, while
  detailed operational syntax often belongs to command pages.
- Commands need operational coverage and enough implementation detail to
  support troubleshooting.
- Functionalities may need all views when they carry user-facing,
  methodological, and technical consequences.
- Workflows should be narrative and procedural; implementation details
  are included only when they clarify the workflow.

------------------------------------------------------------------------

## 6. Non-Redundancy Rule

Create a page only when it answers a non-redundant question.

Do not create all possible views merely because the matrix permits them.

Examples:

- A command Research Context page is unnecessary if the module Research
  Context already explains the methodological issue.
- A module Usage Guide is unnecessary if all module-level operation is
  better handled by command Usage Guides.
- A feature page should not repeat full command syntax unless users need
  that syntax for orientation.

------------------------------------------------------------------------

## 7. Object Discovery

When sweeping a repository, look for objects in:

- CLI registries, parser files, and dispatch tables
- web-app action menus and handlers
- source-code package structure
- configuration schemas and defaults
- generated examples and example manifests
- tests
- README files and existing manuals
- data directories, templates, and output artifacts
- maintainer notes

The first output should be an object inventory, not drafted manual
pages.

The inventory should classify likely objects, cite source anchors, list
recommended views, and surface uncertainties for human response.

------------------------------------------------------------------------

## 8. Human Review Flags

Documentation objects and views should carry review priority when
needed.

High-review topics commonly include:

- privacy and de-identification language
- methodological claims
- validation, reliability, and threshold interpretation
- output interpretation
- workflow-order recommendations
- security or data-governance claims

Medium-review topics commonly include:

- command syntax
- configuration defaults
- output filenames
- web-app availability
- generated example layout

Low-review topics commonly include:

- navigation pages
- technical composition notes
- source-verified command summaries

Review priority should follow the risk of misleading users, not the
length of the page.

------------------------------------------------------------------------

## 9. Optional Metadata

Manual pages may eventually use front matter to support composition.

Example:

```yaml
---
object_type: command
object_id: transcripts.tabularize
module_id: transcripts
view: quickstart
view_order: 10
source_manual: authored
---
```

Generated views should use stable metadata when possible.

Authored pages should not adopt front matter piecemeal unless the
repository has a composition layer that requires it. Add metadata in a
dedicated composition pass.

------------------------------------------------------------------------

## 10. Summary

IRIDIC manuals are organized by object and view:

- objects identify what is being documented
- views identify the reader question being answered

This framework gives human maintainers and LLM assistants a shared map
for sweeping a repository, planning files, drafting pages, and reviewing
manual content without collapsing everything into one large document.
