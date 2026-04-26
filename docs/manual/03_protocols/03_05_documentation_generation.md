# IRIDIC Codex-Ready Documentation Generation Protocol

## Overview

This protocol provides a reusable workflow for using Codex-like tools to draft, update, and maintain repository manuals according to the IRIDIC documentation ontology.

It is designed to help automated coding assistants scan a repository, identify documentation objects, and generate segmented Markdown files using consistent documentation views.

This protocol assumes the IRIDIC ontology defined in the companion policy document:

- **Objects**: Modules, Commands, Functionalities, Workflows
- **Views**: Quickstart, Usage Guide, Research Context, Implementation Notes

---

## 1. Purpose

The purpose of this protocol is to support automated documentation generation while preserving human review, conceptual accuracy, and repository-specific judgment.

Codex-like tools may assist with:

1. Identifying user-facing commands and webapp actions
2. Mapping source files to documentation objects
3. Drafting Markdown files in the appropriate view format
4. Updating existing documentation after code changes
5. Highlighting areas requiring human review

Codex-like tools should not be treated as final methodological authorities. Generated documentation must be reviewed by the repository maintainer before release.

---

## 2. Recommended Inputs

Before running a documentation-generation pass, provide the assistant with as many of the following as possible:

```text
Repository root
src/ directory
pyproject.toml
README.md
CLI entry points
Streamlit or webapp files
Configuration templates
Example input/output files
Existing manual directory, if present
```

Optional but helpful:

```text
tests/ directory
docs/ directory
example_io/ directory
CHANGELOG.md
CONTRIBUTING.md
```

---

## 3. Documentation Generation Workflow

### Step 1: Repository Survey

The assistant should first inspect the repository structure and identify likely documentation targets.

It should look for:

- CLI dispatch files
- argparse or Typer/Click definitions
- Streamlit UI actions
- configuration files
- public functions
- modules under `src/`
- example input/output files
- existing documentation patterns

The output of this step should be an inventory, not drafted documentation.

---

### Step 2: Object Inventory

The assistant should classify documentation targets into the four IRIDIC object types.

| Object Type | Identification Rule |
|---|---|
| Module | A cohesive source-code or user-facing domain |
| Command | A discrete CLI command or webapp operation |
| Functionality | A cross-cutting behavior used by multiple modules or commands |
| Workflow | A multi-step applied process combining several operations |

The assistant should produce a proposed object inventory before drafting files.

---

### Step 3: View Assignment

For each object, assign the appropriate documentation views.

| Object Type | Quickstart | Usage Guide | Research Context | Implementation Notes |
|---|---:|---:|---:|---:|
| Module | Required | Optional | Required | Required |
| Command | Required | Required | Optional | Required |
| Functionality | Required | Usually | Usually | Usually |
| Workflow | Required | Required | Light/Required | Optional |

The assistant should not automatically create all possible files. It should only generate views that provide non-redundant value.

---

### Step 4: File Plan

Before writing documentation, the assistant should propose a file plan.

Example:

```text
manual/
  modules/
    transcripts/
      quickstart.md
      research_context.md
      implementation_notes.md
      commands/
        tabularize/
          quickstart.md
          usage_guide.md
          implementation_notes.md
  functionalities/
    blinding/
      quickstart.md
      usage_guide.md
      research_context.md
      implementation_notes.md
  workflows/
    minimal_pipeline.md
```

The maintainer should review the file plan before broad documentation generation.

---

### Step 5: Draft Markdown Files

After the file plan is accepted, the assistant may draft Markdown files.

Each file should:

- use the correct view template
- avoid unsupported claims
- cite or point to relevant source files when possible
- flag uncertain areas with `TODO:` markers
- avoid duplicating material already covered at a higher level

---

### Step 6: Human Review

The maintainer should review generated files for:

- accuracy
- tone
- methodological claims
- command syntax
- configuration defaults
- output paths
- missing edge cases
- excessive duplication

Generated documentation should not be treated as authoritative until reviewed.

---

## 4. View Templates

### 4.1 Quickstart Template

Use for minimal action summaries.

```md
# Quickstart: {Object Name}

## Description

{One- to three-sentence summary.}

## Command or Action

```bash
{command here}
```

## Required Inputs

- `{input}`: {description}

## Outputs

- `{output}`: {description}

## Key Settings

| Setting | Default | Description |
|---|---:|---|
| `{setting}` | `{default}` | {description} |

## Minimal Example

```bash
{minimal example command}
```

## Notes

- {brief note}
```

---

### 4.2 Usage Guide Template

Use for operational detail.

```md
# Usage Guide: {Object Name}

## Purpose

{Explain what the user can accomplish.}

## Basic Usage

```bash
{basic command}
```

## Arguments

| Argument | Required | Description |
|---|---:|---|
| `{argument}` | Yes/No | {description} |

## Configuration Options

| Setting | Default | Description |
|---|---:|---|
| `{setting}` | `{default}` | {description} |

## Input Requirements

{Describe required file types, sheets, columns, naming conventions, or folder structure.}

## Output Structure

{Describe generated files, directories, sheets, and key columns.}

## Common Variants

### Variant 1: {Name}

```bash
{example}
```

## Common Problems

| Problem | Likely Cause | Suggested Fix |
|---|---|---|
| {problem} | {cause} | {fix} |

## TODO

- {items requiring maintainer review}
```

---

### 4.3 Research Context Template

Use for methodological and scientific rationale.

```md
# Research Context: {Object Name}

## Role in a Research Workflow

{Explain how this object supports research practice.}

## Methodological Rationale

{Explain why this operation matters for rigor, reproducibility, validity, efficiency, or transparency.}

## Best Practices

- {best practice}

## Limitations

- {limitation}

## Interpretation Notes

{Explain how users should or should not interpret outputs.}

## TODO

- {claims requiring citation, review, or expansion}
```

---

### 4.4 Implementation Notes Template

Use for technical transparency.

```md
# Implementation Notes: {Object Name}

## Source Files

- `{path}`: {role}

## Execution Flow

1. {step}
2. {step}
3. {step}

## Key Functions or Classes

| Function/Class | Location | Role |
|---|---|---|
| `{name}` | `{path}` | {description} |

## Data Flow

```text
{input} -> {processing step} -> {output}
```

## Validation and Preflight Checks

- {check}

## Edge Cases

- {edge case}

## Failure Modes

| Failure Mode | Likely Cause | Handling |
|---|---|---|
| {failure} | {cause} | {handling} |

## Extension Points

- {how a developer might modify or extend this behavior}

## TODO

- {items requiring maintainer review}
```

---

## 5. Prompt Templates

### 5.1 Repository Survey Prompt

```text
You are helping generate IRIDIC-style repository documentation.

Please inspect this repository and produce a documentation object inventory. Do not draft manual files yet.

Classify likely documentation targets into:
1. Modules
2. Commands
3. Functionalities
4. Workflows

For each proposed object, include:
- proposed object name
- object type
- relevant source files
- relevant CLI commands or webapp actions, if any
- recommended documentation views
- uncertainties or questions for human review

Use the IRIDIC object/view ontology:
- Objects: Module, Command, Functionality, Workflow
- Views: Quickstart, Usage Guide, Research Context, Implementation Notes

Apply this view matrix:
- Modules: Quickstart, Research Context, Implementation Notes required; Usage Guide optional
- Commands: Quickstart, Usage Guide, Implementation Notes required; Research Context optional
- Functionalities: most views usually appropriate if non-redundant
- Workflows: Quickstart and Usage Guide required; Research Context light/required; Implementation Notes optional
```

---

### 5.2 File Plan Prompt

```text
Using the approved object inventory, propose a documentation file plan.

Do not write file contents yet.

Use a hypermodular structure where each object may contain separate Markdown files for its views.

Only include a view file if it answers a non-redundant question.

For each file, provide:
- path
- object type
- view type
- one-sentence purpose
- relevant source files
- whether human review is especially important

Prefer paths like:
manual/modules/{module}/...
manual/modules/{module}/commands/{command}/...
manual/functionalities/{functionality}/...
manual/workflows/{workflow}.md
```

---

### 5.3 Command Documentation Prompt

```text
Please draft IRIDIC-style documentation for the command `{command}`.

Generate the following views unless one would be redundant:
1. quickstart.md
2. usage_guide.md
3. implementation_notes.md
4. research_context.md only if the command has distinct methodological stakes

Use the source files listed below:
{source files}

Requirements:
- Keep Quickstart brief and action-oriented.
- Put operational options in Usage Guide, not Implementation Notes.
- Put functions, classes, data flow, validation, and failure modes in Implementation Notes.
- Do not make unsupported methodological claims.
- Add `TODO:` markers where human review is needed.
- Do not duplicate module-level research context unless command-specific interpretation differs.
```

---

### 5.4 Module Documentation Prompt

```text
Please draft IRIDIC-style documentation for the `{module}` module.

Generate:
1. quickstart.md
2. research_context.md
3. implementation_notes.md
4. usage_guide.md only if module-level usage is not redundant with command-level usage

Use the source files listed below:
{source files}

Requirements:
- Treat the module as a cohesive operational domain.
- Describe the commands it contains and how they relate.
- Use Research Context for broad methodological framing.
- Use Implementation Notes for architecture and module-level data flow.
- Do not provide exhaustive command syntax unless this is a module-level Quickstart.
- Add `TODO:` markers where human review is needed.
```

---

### 5.5 Functionality Documentation Prompt

```text
Please draft IRIDIC-style documentation for the cross-cutting functionality `{functionality}`.

This functionality appears across multiple modules or commands:
{list modules/commands}

Generate views that provide non-redundant value:
1. quickstart.md
2. usage_guide.md
3. research_context.md
4. implementation_notes.md

Requirements:
- Explain which commands are affected.
- Explain how users encounter this functionality.
- Explain why the behavior is centralized or reused.
- Explain the shared implementation logic.
- Avoid repeating command-specific usage details unless necessary.
- Add `TODO:` markers where human review is needed.
```

---

### 5.6 Workflow Documentation Prompt

```text
Please draft an IRIDIC-style workflow document for `{workflow}`.

This workflow should show how a user combines multiple commands to accomplish a practical goal.

Include:
1. scenario
2. prerequisites
3. step-by-step procedure
4. commands used
5. expected inputs
6. expected outputs
7. recommended checks
8. common variations
9. light research/methodological rationale where relevant

Avoid implementation details unless they help the user understand the workflow.

Add `TODO:` markers where human review is needed.
```

---

### 5.7 Update Existing Documentation Prompt

```text
Please update the existing IRIDIC-style documentation after the following code changes:

{summary of changes}

Inspect the relevant source files and update only documentation sections affected by the change.

Requirements:
- Preserve existing structure and tone.
- Do not rewrite unrelated sections.
- Update command syntax, configuration defaults, input requirements, output paths, and implementation notes as needed.
- Add `TODO:` markers if the code behavior is ambiguous.
- Provide a brief changelog of documentation edits made.
```

---

## 6. Rules for Automated Drafting

### 6.1 Do Not Overclaim

The assistant must not invent methodological validation, software guarantees, or output interpretations not supported by the code or existing documentation.

Use:

```text
TODO: Confirm whether this interpretation is intended.
```

instead of unsupported certainty.

---

### 6.2 Separate Usage from Implementation

Operational instructions belong in Usage Guides.

Internal mechanics belong in Implementation Notes.

If the assistant is unsure where to place a detail, prefer Usage Guide for user-facing behavior and Implementation Notes for source-code behavior.

---

### 6.3 Avoid Redundancy

Do not repeat module-level research context in every command.

Command-level Research Context should be generated only when the command has distinct methodological stakes.

---

### 6.4 Preserve Hypermodularity

Separate Markdown files are encouraged when they improve webapp navigation, selective rendering, or TL;DR access.

However, a file should not be created merely to satisfy symmetry.

---

### 6.5 Prefer Explicit TODOs

If a detail cannot be confirmed from source code, mark it clearly.

Examples:

```text
TODO: Confirm default output directory.
TODO: Confirm whether this argument is exposed in the CLI.
TODO: Add citation or methodological reference.
TODO: Verify this behavior against current tests.
```

---

## 7. Recommended Review Checklist

Before accepting generated documentation, confirm:

- [ ] Command syntax is accurate
- [ ] Configuration defaults are accurate
- [ ] Input paths and output paths are accurate
- [ ] Required columns/sheets/files are accurate
- [ ] Examples run successfully
- [ ] Research claims are appropriately cautious
- [ ] Implementation notes match current code
- [ ] TODOs have been resolved or intentionally retained
- [ ] File organization matches the approved ontology
- [ ] Content is not duplicated unnecessarily

---

## 8. Recommended Commit Strategy

For large documentation generation, use staged commits:

```text
1. Add documentation ontology policy
2. Add documentation generation protocol
3. Add object inventory
4. Add module-level documentation
5. Add command-level documentation
6. Add functionality documentation
7. Add workflow documentation
8. Review and clean TODOs
```

This makes generated documentation easier to review, revert, and revise.

---

## 9. Minimal First-Pass Workflow

For a new repository, start small.

Recommended first pass:

```text
1. Survey src/
2. Identify modules and commands
3. Draft one module overview
4. Draft one command Quickstart
5. Draft one command Usage Guide
6. Draft one command Implementation Notes
7. Review manually
8. Generalize to additional commands
```

This avoids generating a large manual before the ontology has been tested against the repository.

---

## 10. Summary

This protocol turns the IRIDIC documentation ontology into a practical workflow for automated documentation generation.

The core rule is:

> Generate documentation by object and view, but only create files that answer non-redundant questions.

The protocol supports:

- structured manual generation
- webapp-friendly hypermodularity
- human review
- Codex-like automation
- cautious methodological framing
- technical transparency
