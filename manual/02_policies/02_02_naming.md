# Repository Naming Policy

**Project:** IRIDIC -- Idiosyncratic Repository of Initialization &
Development Itineraries for Codebases\
**Document:** naming.md\
**Last Updated:** 2026-02-21

------------------------------------------------------------------------

## 1. Purpose

This document defines guiding principles and procedural safeguards for
naming repositories, Python libraries, and associated software tools.

Naming is treated as both: 
- A **technical constraint problem**
(uniqueness, discoverability, packaging compatibility), and
- An **intellectual positioning exercise** (accurate representation of
scope, tone, and intent).

The goal is not perfection, but principled iteration toward clarity and
stability.

------------------------------------------------------------------------

## 2. Core Principles

### 2.1 Substantial Orthographic Distinctiveness

A proposed name must not substantially collide with existing
software---especially on PyPI.

**Operational criterion:**\
If the case-sensitive Levenshtein edit distance from an existing
software package is ≲ 2, further iteration is required.

Rationale:
- Prevents user confusion
- Avoids namespace disputes 
- Protects long-term identity
- Preserves scholarly and software credibility

Collision checks must include:
- PyPI search
- GitHub search
- General web search
- Domain name availability (when relevant)

------------------------------------------------------------------------

### 2.2 No Hyphenated Library Names (Forward Policy)

Moving forward, library names should avoid hyphenation.

Example (legacy): - `pip install rascal-speech`

Preferred style:
- `pip install clatr`
- `pip install taalcr`
- `pip install alastr`

Rationale:
- Cleaner imports
- Fewer user errors
- Reduced packaging friction
- Greater conceptual cohesion

Note: RASCAL predates this policy and is grandfathered in.

------------------------------------------------------------------------

### 2.3 Acronym Purity

Every letter in an acronym ideally corresponds to a content word.

Allowed:
- Functor words (for, to, and, in, of, etc.) may be used freely
and are not required to map to letters.
- Occasional orthographic adjustments for pronounceability are acceptable.
- Syllabic consonants that deviate orthography of English words (e.g., the 'R' in CLATR)

Avoid:
- Forced letter stuffing
- Backronyms that misrepresent scope
- Empty symbolic letters

The acronym should feel structurally honest.

------------------------------------------------------------------------

### 2.4 Accurate Character Representation

The name must reflect what the software *actually is*.

Avoid:
- Overstatement (inflated claims)
- Understatement (false modesty)
- Vague generalities

Priority:
- Faithful description of function
- Honest scope boundaries
- Clear positioning within ecosystem

The name should survive contact with:
- Reviewers
- Users
- Supervisors
- Future self

------------------------------------------------------------------------

### 2.5 Whimsy With Awareness

Whimsy is embraced.

Playful names are acceptable when:
- The software itself is serious and robust
- The documentation is rigorous
- The acronym is defensible (according to above principles)
- The tone does not undermine credibility

Whimsy is stylistic---not structural.

The name must withstand scrutiny even if stripped of its humor.

------------------------------------------------------------------------

## 3. Conceptual Fit

An ideal name:

-   Relates meaningfully to the program's purpose
-   Sounds like a software tool
-   Is pronounceable
-   Is memorable
-   Is typographically clean
-   Scales with ecosystem growth

Names should feel:

-   Intentional, not accidental
-   Designed, not improvised
-   Stable, not provisional

------------------------------------------------------------------------

## 4. Iterative Process

Naming is an iterative optimization problem.

Typical process:

1.  Generate candidate acronyms
2.  Check collision distance
3.  Check semantic clarity
4.  Check packaging viability
5.  Evaluate tone
6.  Let it sit
7.  Re-evaluate
8.  Seek LLM feedback (optional but typical)
9.  Stop at diminishing returns

Perfectionism is recognized as unproductive.\
Iteration continues until marginal improvement is negligible.

------------------------------------------------------------------------

## 5. Ecosystem Coherence

Repository names should coexist coherently within the broader project
ecosystem.

Consider:
- Visual similarity across tools
- Structural symmetry (e.g., ALASTR, TAALCR, RASCAL)
- Functional differentiation
- Hierarchical relationships (umbrella vs. subtool)
- Long-term publication strategy

The name should not accidentally obscure authorship boundaries or
intellectual positioning.

------------------------------------------------------------------------

## 6. Packaging & Technical Constraints

Before finalizing:

-   Confirm PyPI availability
-   Confirm GitHub org availability
-   Confirm import safety (valid module name)
-   Confirm no reserved keyword conflicts
-   Confirm no accidental profanity or unintended cross-language meaning
-   Test local install and import

If any of the above fail → iterate.

------------------------------------------------------------------------

## 7. Tone & Professional Signaling

A name should:

-   Signal competence & intentionality
-   Avoid insecurity, self-aggrandizement, & apologetic understatement

The aim is quiet precision.

------------------------------------------------------------------------

## 8. Documentation Requirement

Every repository must include:

-   A README that expands the acronym
-   Versioning from first commit (e.g., 0.0.1a1)

and ideally includes:

-   A short explanation of the naming rationale
-   A CITATION.cff file (even pre-publication)


Naming is part of scholarly identity.

------------------------------------------------------------------------

## 9. Legacy Exception: RASCAL

RASCAL predates this formal naming policy.

While hyphenation exists in `rascal-speech`, there appears to be no
orthographic collision within the SLP or aphasiology space. The name is
retained for continuity and published precedent.

Future repositories follow this policy strictly.

------------------------------------------------------------------------

## 10. Final Heuristic

If the name:

-   Is orthographically distinct
-   Is acronymically honest
-   Is semantically accurate
-   Is technically viable
-   Is ecosystem-consistent
-   Feels stable after multiple passes

→ It is sufficient.

The standard is not perfection but durability.
