# Testing Policy

## 1. Purpose

This document defines the standard testing conventions for Python
repositories in the IRIDIC ecosystem.

The goals are:

-   make expected behavior explicit
-   catch regressions before release or deployment
-   keep research software reproducible across local machines and time
-   make test locations predictable across repositories
-   support LLM-assisted development with verifiable execution records

Testing is not treated as ornamental coverage. It is part of the
research infrastructure that allows tools to be refactored, packaged,
released, and reused with confidence.

------------------------------------------------------------------------

## 2. Default Test Framework

Python projects should use **pytest** as the default test framework.

Pytest is preferred because it:

-   supports concise function-based tests
-   provides strong assertion introspection
-   works well with fixtures and temporary directories
-   integrates cleanly with `src/`-layout packages
-   supports both focused local tests and full regression suites

Repository-level pytest behavior may be configured in `pytest.ini`,
`pyproject.toml`, or another standard pytest configuration location.
The chosen location should be clear, committed, and consistent within a
repository.

------------------------------------------------------------------------

## 3. Test Directory Structure

All test code should live under:

    tests/

The `tests/` directory should generally mirror the structure of `src/`.
This makes it easy to locate the tests associated with a source module.

Example source layout:

    src/
    `-- package_name/
        |-- cli.py
        |-- transcripts/
        |   |-- cleanup.py
        |   `-- parsing.py
        `-- utils/
            `-- paths.py

Corresponding test layout:

    tests/
    |-- test_cli.py
    |-- transcripts/
    |   |-- test_cleanup.py
    |   `-- test_parsing.py
    `-- utils/
        `-- test_paths.py

For larger repositories, tests may include additional subdirectories for
broader behaviors:

    tests/
    |-- integration/
    |-- regression/
    `-- fixtures/

These directories should be added only when they clarify the test suite.
The default preference is still to keep tests close to the source
structure they exercise.

------------------------------------------------------------------------

## 4. Test Naming

Test files should use the pytest naming pattern:

    test_*.py

Test functions should use:

    test_*

Names should describe the behavior being protected, not merely the
implementation being called.

Preferred:

    test_parser_preserves_speaker_labels
    test_output_path_is_created_when_missing

Avoid:

    test_parser
    test_function_1

Clear test names make failures readable during development and in
future CI logs.

------------------------------------------------------------------------

## 5. Scope of Tests

IRIDIC projects should distinguish between several useful test scopes.

### Unit Tests

Unit tests check a small function or class in isolation.

They should be:

-   fast
-   deterministic
-   independent of external services
-   easy to run during active editing

### Integration Tests

Integration tests check that multiple modules work together correctly.

They are appropriate for:

-   CLI execution paths
-   pipeline orchestration
-   file input/output workflows
-   database interactions
-   web interface wrappers over backend code

### Regression Tests

Regression tests protect against bugs that have already occurred.

When a defect is fixed, a test should be added when practical so that
the same defect is unlikely to return silently.

### Documentation and Example Tests

Examples in documentation, README files, or rendered manuals may require
tests when they function as executable user guidance.

For research software, examples are often part of the public interface.
If users are expected to copy a command or follow a documented workflow,
that command or workflow should be periodically verified.

------------------------------------------------------------------------

## 6. Test Data and Fixtures

Small test inputs may be committed under `tests/fixtures/` or an
equivalent local fixture directory.

Fixtures should be:

-   minimal
-   purpose-specific
-   safe to redistribute
-   independent of user-specific absolute paths

Large datasets, private data, generated outputs, and machine-specific
artifacts should not be committed as ordinary test fixtures. When tests
require external or archival data, the retrieval or preparation process
should be documented explicitly.

Tests should prefer temporary directories for generated files. This
keeps the working tree clean and reduces the risk that tests pass only
because of stale local artifacts.

------------------------------------------------------------------------

## 7. Standard Test Execution

Each repository should provide one clear default command for running the
test suite.

For simple projects, this may be:

    python -m pytest tests

For repositories using Anaconda environments on Windows, a tracked helper
script is often preferable:

    .\scripts\run_tests.ps1 tests

The helper script should call the intended environment's Python
interpreter directly and forward arguments to pytest. This makes the test
entry point reproducible for both the human developer and LLM-assisted
sessions.

Focused tests should use the same entry point with a narrower path:

    .\scripts\run_tests.ps1 tests/transcripts/test_parsing.py

The important principle is that the repository should have an
authoritative, documented way to run tests. Developers and assistants
should not need to rediscover the correct environment invocation from
scratch each time.

------------------------------------------------------------------------

## 8. Repository-Local Command Notes

Repositories may include local command guidance for development agents
and future maintainers.

In DIAAD, for example:

    .codex-local/COMMANDS.md

records project-specific operational facts such as:

-   the repository root
-   the expected Conda environment
-   the preferred pytest command
-   known command forms to avoid
-   escalation or retry guidance for sandboxed sessions

The function of this file is not to replace the public manual. It is a
local operations note: a compact, practical source of truth for running
commands correctly in that repository.

This kind of file is useful because LLM-assisted development benefits
from explicit local instructions. It reduces accidental command drift,
prevents misleading test claims, and preserves practical knowledge that
might otherwise live only in memory.

------------------------------------------------------------------------

## 9. Test Runner Helper Scripts

Repositories may also include a tracked test runner script.

In DIAAD, for example:

    scripts/run_tests.ps1

is a small PowerShell wrapper that:

-   accepts pytest arguments
-   locates the DIAAD Python interpreter
-   allows an environment variable override
-   invokes `python -m pytest`
-   exits with pytest's status code

This pattern has several advantages.

First, it avoids depending on shell-specific or Conda-wrapper behavior
when the goal is simply to run pytest. Second, it gives every developer
and assistant the same command surface. Third, it makes failure states
clear: if pytest did not actually start and return success, the test run
must not be reported as passing.

The exact helper script may vary by repository, but its responsibilities
should remain narrow. It should run tests, forward arguments, and return
the correct exit code. It should not hide failures or perform unrelated
setup work silently.

------------------------------------------------------------------------

## 10. Development Workflow

During ordinary development:

1.  Add or update tests near the source behavior being changed.
2.  Run focused tests for the affected module or workflow.
3.  Run the full test suite before merging to `main` or preparing a
    release.
4.  Document any test limitations or skipped cases.

Before release or deployment, verify at minimum:

-   full pytest suite passes
-   CLI entry points still work
-   documented example commands remain accurate
-   packaging or installation changes have been tested in the intended
    environment

This aligns testing with IRIDIC's broader emphasis on reproducible,
transparent, durable research software.

------------------------------------------------------------------------

## 11. LLM-Assisted Testing Discipline

When an LLM assistant runs tests, it should report the actual command
used and whether pytest completed successfully.

Do not claim test success when:

-   pytest did not start
-   the command failed before reaching pytest
-   only import discovery ran
-   a sandbox or environment failure prevented execution
-   tests were skipped in a way that leaves the changed behavior
    unverified

If a command fails for environmental reasons, the failure should be
reported plainly. If a project provides a helper script, that helper
should be preferred over ad hoc environment commands.

The policy is simple: test claims should describe observed test
execution, not intended test execution.

------------------------------------------------------------------------

## 12. Summary

IRIDIC repositories should use pytest, keep tests under `tests/`, and
structure that directory so it mirrors `src/` wherever practical.

Project-local command notes and helper scripts, such as DIAAD's
`.codex-local/COMMANDS.md` and `scripts/run_tests.ps1`, support this
policy by making test execution explicit, repeatable, and easier to
verify across human and LLM-assisted development sessions.
