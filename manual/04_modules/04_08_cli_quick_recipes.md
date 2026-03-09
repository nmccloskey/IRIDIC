
# Common CLI Tasks (Quick Recipes)

This section provides **quick command-line recipes** for common IRIDIC manual tasks.

The commands below assume the standard manual directory:

```
manual/
```

If your manual directory has a different name, replace `manual` accordingly.

---

# Inspecting a Manual

## View the manual tree

```
iridic tree
```

Displays the generated directory tree of the manual.

Example:

```
IRIDIC/
├── 01_introduction.md
├── 02_installation.md
├── 03_workflow/
│   ├── 03_01_overview.md
│   └── 03_02_cli_commands.md
```

---

## Search the manual

```
iridic search "installation"
```

Searches titles and content across manual files.

Limit the number of results:

```
iridic search "database" --limit 10
```

---

## Inspect the indexed manual

```
iridic index
```

Shows summary statistics such as:

- number of indexed files
- number of top‑level sections

Show the list of indexed files:

```
iridic index --show-files
```

---

# Preparing a Manual

## Check documentation characters

```
iridic chars manual
```

Runs character and formatting validation across documentation files.

---

## Detect trailing whitespace

```
iridic chars manual --check-trailing
```

---

## Remove trailing whitespace

```
iridic chars manual --strip-trailing
```

---

## Detect Windows line endings

```
iridic chars manual --check-line-endings
```

---

## Normalize line endings

Convert to LF:

```
iridic chars manual --fix-line-endings lf
```

Convert to CRLF:

```
iridic chars manual --fix-line-endings crlf
```

---

## Detect non‑ASCII characters

```
iridic chars manual --report-nonascii
```

Treat non‑ASCII characters as errors:

```
iridic chars manual --fail-on-nonascii
```

---

# Generating Navigation

## Generate the manual outline

```
iridic outline manual
```

Creates:

```
manual/00_outline.md
```

---

## Specify manual title and version

```
iridic outline manual   --title "IRIDIC Instruction Manual"   --version 0.1.0
```

---

## Generate the outline only if missing

```
iridic outline manual --if-missing-only
```

---

# Building the Manual PDF

## Compile the manual

```
iridic pdf manual
```

---

## Compile using a YAML configuration

```
iridic pdf manual --yaml manual/manual_pdf.yaml
```

This is the **recommended workflow**.

---

## Specify output location

```
iridic pdf manual   --yaml manual/manual_pdf.yaml   --output dist/manual.pdf
```

---

## Adjust page margins

```
iridic pdf manual --margin 0.8in
```

---

## Disable the table of contents

```
iridic pdf manual --no-toc
```

---

## Change TOC depth

```
iridic pdf manual --toc-depth 2
```

---

## Include the outline in the PDF

```
iridic pdf manual --include-outline
```

---

## Pass additional arguments to Pandoc

```
iridic pdf manual   --yaml manual/manual_pdf.yaml   --extra-pandoc-arg "--citeproc"
```

---

# Controlling Preflight Checks

The PDF command normally runs validation steps before compilation.

---

## Skip outline generation

```
iridic pdf manual --skip-outline
```

---

## Force outline rebuild

```
iridic pdf manual --rebuild-outline
```

---

## Skip character validation

```
iridic pdf manual --skip-chars
```

---

## Run compilation non‑interactively

```
iridic pdf manual --non-interactive
```

---

## Force compilation even if issues are detected

```
iridic pdf manual --force
```

---

# Full Recommended Workflow

A typical manual build sequence:

```
iridic chars manual --check-trailing
iridic outline manual
iridic pdf manual --yaml manual/manual_pdf.yaml
```

This sequence:

1. validates documentation
2. ensures the outline exists
3. compiles the manual PDF

---

# Summary

These quick recipes cover the most common IRIDIC manual workflows:

- exploring manual structure
- validating documentation formatting
- generating navigation outlines
- compiling distributable PDF manuals

For a complete list of CLI options, see the **CLI Command Reference** section.
