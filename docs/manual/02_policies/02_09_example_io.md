# IRIDIC Policy: Example Files and `example_io` Manual Architecture

## Overview

This document defines the policy for managing **example input/output files** and the construction of the **`example_io` manual** within IRIDIC-compliant repositories (e.g., DIAAD, TAALCR, ALASTR).

The goal is to ensure:

* **Clarity**: Users can see concrete examples of each module’s behavior
* **Reproducibility**: Example workflows reflect real execution
* **Maintainability**: Documentation is modular and partially auto-generated
* **Extensibility**: Codex or similar tools can programmatically expand coverage

---

## Core Design Principles

### 1. Single Source of Truth (SSOT)

* Structured specifications (e.g., `.yaml`, `.json`) define:

  * Inputs
  * Outputs
  * Transformations
* Markdown documentation is **derived**, not authoritative

---

### 2. Deliberate Duplication (Controlled)

We intentionally maintain two parallel representations:

| Layer            | Purpose                             |
| ---------------- | ----------------------------------- |
| `spec/`          | Machine-readable definitions (SSOT) |
| `rendered_docs/` | Human-readable Markdown (derived)   |

This duplication is:

* **Intentional**
* **Automated where possible**
* **Auditable**

---

### 3. Separation of Concerns

* **Assets**: Raw example data
* **Specs**: Structured definitions of transformations
* **Docs**: Rendered explanations and walkthroughs

---

## Directory Structure

A canonical structure is:

```
assets/
└── example_io/
    ├── transcripts/
    │   ├── input/
    │   └── output/
    ├── cus/
    └── ...

spec/
└── example_io/
    ├── transcripts_tabularize.yaml
    └── ...

rendered_docs/
└── example_io/
    ├── 01_overview.md
    ├── transcripts/
    │   └── tabularize.md
    └── ...

docs/
└── manual/
    └── (compiled via IRIDIC)
```

---

## The `example_io` Manual

### Purpose

The `example_io` manual provides:

* End-to-end examples of module behavior
* Concrete input/output artifacts
* Interpretable representations of internal transformations

---

### Composition

The manual consists of:

#### 1. Built-in Markdown Files (Static)

Example:

```
rendered_docs/example_io/01_overview.md
```

These:

* Are **handwritten**
* Provide conceptual framing
* Do **not** derive from specs

---

#### 2. Generated Markdown Files (Dynamic)

Example:

```
rendered_docs/example_io/transcripts/tabularize.md
```

These are:

* **Programmatically generated**
* Derived from `spec/example_io/*.yaml`
* Synchronized with actual assets

---

## Example: `transcripts tabularize`

### Specification (SSOT)

Located at:

```
spec/example_io/transcripts_tabularize.yaml
```

Defines:

* Input `.cha` files
* Output transcript tables
* Expected sheets (`samples`, `utterances`)

---

### Assets

Located at:

```
assets/example_io/transcripts/
```

Includes:

* Raw CHAT files
* Generated `.xlsx` transcript tables

---

### Rendered Documentation

Located at:

```
rendered_docs/example_io/transcripts/tabularize.md
```

Must include:

#### 1. Project Directory Tree

```text
example_io/
└── transcripts/
    ├── input/
    │   └── sample1.cha
    └── output/
        └── transcript_tables.xlsx
```

---

#### 2. Input Representation

* Snippet of `.cha` file
* Minimal but representative

---

#### 3. Output Representation

**All sheets must be shown**, especially:

##### Samples Sheet

| sample_id | speaking_time |
| --------- | ------------- |
| S1        | 45.2          |

---

##### Utterances Sheet

| utterance_id | sample_id | utterance          |
| ------------ | --------- | ------------------ |
| U1           | S1        | The boy is running |

---

---

#### 4. Notes

* Explain transformations
* Highlight design decisions (e.g., position vs position_sub)
* Keep concise

---

## Rendering Pipeline

### Flow

```
spec (.yaml)
    ↓
rendering functions
    ↓
rendered_docs (.md)
    ↓
IRIDIC manual builder
    ↓
final manual (CLI + Streamlit)
```

---

### Responsibilities

| Component | Responsibility           |
| --------- | ------------------------ |
| `spec/`   | Defines truth            |
| renderer  | Converts spec → Markdown |
| IRIDIC    | Aggregates manuals       |
| assets    | Provide real data        |

---

## Rules for Generated Docs

1. **No manual edits**

   * Files in `rendered_docs/` should be treated as derived artifacts

2. **Deterministic output**

   * Same spec + assets → identical `.md`

3. **Minimal verbosity**

   * Focus on structure, not narrative

4. **Always include I/O**

   * At least one full input/output example per module

---

## Rules for Assets

1. Must be:

   * Small
   * Representative
   * Non-sensitive

2. Must reflect:

   * Real pipeline outputs
   * Current schema

3. Should be:

   * Regenerable via CLI where possible

---

## Integration with IRIDIC

The `example_io` manual is treated as:

* A **standard IRIDIC manual**
* Located under `rendered_docs/example_io/`
* Included via:

  * CLI (`iridic manual pdf`)
  * Streamlit viewer

---

## Codex Integration Strategy

Codex (or similar tools) should:

1. Read:

   * `spec/example_io/*.yaml`

2. Generate:

   * Markdown files in `rendered_docs/`

3. Validate:

   * Asset existence
   * Schema consistency

---

## Incremental Development Strategy

Start with:

* One module:

  * `transcripts tabularize`

Then expand:

1. Add new spec file
2. Add example assets
3. Generate `.md`
4. Integrate into manual

---

## Non-Goals

This system does **not** aim to:

* Replace full documentation
* Provide exhaustive edge-case coverage
* Serve as a tutorial narrative

It is strictly:

> A **grounded, example-driven reference layer**

---

## Summary

The `example_io` system establishes a disciplined documentation pattern:

* **Specs define truth**
* **Assets demonstrate reality**
* **Docs render interpretation**

This enables:

* Scalable documentation
* Reliable onboarding
* Tight coupling between code and explanation

---

## Future Extensions

* Automated validation of example outputs
* Snapshot testing for `.md` generation
* Multi-module workflow chaining (e.g., transcripts → CU → analysis)
* Optional interactive visualization in Streamlit

---
