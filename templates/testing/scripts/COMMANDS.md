# REPO Codex Command Notes

## General

0. The project root is `<path-to-repo>`; any relative paths in the prompt can be assumed to extend from this root, unless otherwise specified.
1. There is a `repo` conda env available.
2. Please explicitly note any issues you encounter, even if it's not feasible to handle them in the current pass.
3. Any suggestions for improvement are welcome, particularly with respect to best practices in research software development.

## Testing

When testing on Windows in this repo, use the tracked helper:

```powershell
.\scripts\run_tests.ps1 tests
```

Example for focused tests:

```powershell
.\scripts\run_tests.ps1 tests/test_transcripts/test_detabularization.py
```

Avoid `conda run -n repo pytest ...` in Codex sessions unless Conda wrapper behavior itself is being tested. If sandboxed Python spawning fails before pytest starts, retry once, then request escalated execution of the same helper command. Do not claim test success unless pytest actually ran and returned success.
