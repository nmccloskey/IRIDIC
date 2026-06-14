# IRIDIC Documentation Ontology Policy

## Overview

This document defines the structural and conceptual framework for repository documentation within IRIDIC (Idiosyncratic Repository of Initialization & Development Itineraries for Codebases). The goal is to provide a unified, scalable system that supports:

1. **Developers** organizing and maintaining documentation efficiently
2. **Users** accessing information at the appropriate level of detail
3. **Automated systems** (e.g., Codex-like tools) generating and updating documentation programmatically

This framework is based on a dual-axis ontology:

* **Objects**: What is being documented
* **Views**: How the information is presented

---

## Core Ontology

### 1. Objects (Documentation Targets)

Objects define the *unit of documentation*. All documentation content must correspond to one of the following object types:

#### 1.1 Modules

A **module** is a cohesive operational domain containing related commands that act on a shared data representation.

**Examples**

* transcript module
* cus module
* words module

**Purpose**

* Provide high-level conceptual grouping
* Describe system-level workflows and architecture

---

#### 1.2 Commands

A **command** is a discrete, user-invokable operation (CLI or webapp action).

**Examples**

* `transcripts tabularize`
* `cus analyze`
* `words make`

**Purpose**

* Serve as the primary unit of user interaction
* Provide complete operational documentation

---

#### 1.3 Functionalities

A **functionality** is a reusable, cross-cutting behavior applied across multiple modules or commands.

**Examples**

* blinding
* reliability sampling
* transcript parsing

**Purpose**

* Avoid duplication of shared concepts
* Provide centralized explanations of recurring behaviors

---

#### 1.4 Workflows

A **workflow** is a multi-step applied process combining multiple commands and/or modules.

**Examples**

* minimal pipeline
* full analysis pipeline
* reliability workflow

**Purpose**

* Demonstrate real-world usage
* Guide users through multi-step procedures

---

## 2. Views (Documentation Perspectives)

Views define *how information is presented* for each object.

---

### 2.1 Quickstart

**Description**
A minimal, action-oriented summary enabling immediate use.

**Guiding Question**

> What command do I run right now?

**Contents**

* One-line description
* CLI command(s)
* Required inputs
* Outputs
* Key settings (minimal)

---

### 2.2 Usage Guide

**Description**
Detailed operational instructions covering all relevant options and configurations.

**Guiding Question**

> What options do I need and how do they change behavior?

**Contents**

* Expanded description
* Arguments and configuration options
* Variants and edge cases
* Practical examples

---

### 2.3 Research Context

**Description**
Methodological and scientific rationale for using the feature.

**Guiding Question**

> When and why should I use this in a study?

**Contents**

* Role in research workflows
* Theoretical grounding
* Best practices
* Limitations and caveats

---

### 2.4 Implementation Notes

**Description**
Technical explanation of internal behavior and system design.

**Guiding Question**

> How is this implemented and how could I modify it?

**Contents**

* Functions and execution flow
* Data transformations
* Assumptions and constraints
* Failure modes and edge cases

---

## 3. View Requirements by Object Type

Not all objects require all views. The following matrix defines required vs optional views:

| Object Type   | Quickstart | Usage Guide | Research Context | Implementation Notes |
| ------------- | ---------- | ----------- | ---------------- | -------------------- |
| Module        | Required   | Optional    | Required         | Required             |
| Command       | Required   | Required    | Optional         | Required             |
| Functionality | Required   | Usually     | Usually          | Usually              |
| Workflow      | Required   | Required    | Light/Required   | Optional             |

---

## 4. Design Principles

### 4.1 Non-Redundancy

Each view should answer a **distinct question**. Avoid duplicating content across views or object types.

---

### 4.2 Hierarchical Clarity

* **Modules** → define conceptual domains
* **Commands** → define operations
* **Functionalities** → define shared behaviors
* **Workflows** → define real-world usage

---

### 4.3 Boundary Enforcement

Clear separation between views:

* **Usage Guide** = how to use
* **Implementation Notes** = how it works
* **Research Context** = why it matters

---

### 4.4 Hypermodularization with Discipline

Documentation may be split into multiple files per object (e.g., one file per view) to support:

* Webapp navigation
* Incremental rendering
* Selective reading (TL;DR vs deep dive)

However:

> Files should only exist if they provide non-redundant value.

---

### 4.5 Predictable Micro-Structure

All **Quickstart** sections should follow a consistent schema:

```md
**Description**
Brief summary

**Command**
diaad ...

**Inputs**
- ...

**Outputs**
- ...

**Key Settings**
- ...
```

This ensures:

* user clarity
* machine readability
* compatibility with automated documentation generation

---

## 5. File Organization

### 5.1 Modules

```text
manual/
  modules/
    transcript_module/
      quickstart.md
      research_context.md
      implementation_notes.md
      commands/
        transcript_tabularize/
          quickstart.md
          usage_guide.md
          implementation_notes.md
```

---

### 5.2 Functionalities

```text
manual/
  functionalities/
    blinding/
      quickstart.md
      usage_guide.md
      research_context.md
      implementation_notes.md
```

---

### 5.3 Workflows

```text
manual/
  workflows/
    minimal_pipeline.md
    full_pipeline.md
```

---

## 6. Rationale

This ontology is designed to:

### 6.1 Support Multiple Audiences

| Audience    | Needs                |
| ----------- | -------------------- |
| Users       | Quickstart, Usage    |
| Researchers | Research Context     |
| Developers  | Implementation Notes |

---

### 6.2 Enable Automated Documentation (Codex Integration)

The structured separation of:

* objects
* views
* predictable schemas

allows automated systems to:

* parse source code
* generate targeted documentation
* update specific views without affecting others

---

### 6.3 Scale with Project Complexity

As projects grow:

* new commands fit naturally into modules
* shared logic is abstracted into functionalities
* workflows demonstrate integration

---

### 6.4 Maintain Clarity in Complex Systems

By separating:

* *what exists* (objects)
* *how it is explained* (views)

the system avoids:

* monolithic documentation
* duplicated explanations
* user overwhelm

---

## 7. Summary

IRIDIC documentation is built on:

* **Objects**: Module, Command, Functionality, Workflow
* **Views**: Quickstart, Usage Guide, Research Context, Implementation Notes

This structure provides:

* clarity for users
* maintainability for developers
* compatibility with automated documentation systems
