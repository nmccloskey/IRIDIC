# Rename a Conda Environment (Safely and Cleanly)

This protocol documents how to rename a Conda environment using modern Conda versions, along with fallback strategies for older systems.

---

## Overview

Conda supports direct environment renaming starting in:

- **conda >= 4.14.0**

If you are on an older version, see the **Fallback Method** section below.

---

## Prerequisites

Before renaming:

- You **must not** be inside the environment you are renaming.
- You **cannot rename the `base` environment`.**
- You must know the exact current environment name.
- Confirm your Conda version:

```bash
conda --version
```

---

## Method 1 — Direct Rename (Conda ≥ 4.14.0)

### Step 1 — Deactivate the Environment

If the environment is currently active:

```bash
conda deactivate
```

Older systems may require:

- macOS/Linux: `source deactivate`
- Windows (legacy): `deactivate`

Verify you're no longer inside it:

```bash
conda info --envs
```

The active environment is marked with `*`. Ensure your target environment does **not** have it.

---

### Step 2 — Verify the Existing Environment Name

List all environments:

```bash
conda env list
```

or

```bash
conda info --envs
```

Confirm the exact spelling of `old_name`.

---

### Step 3 — Rename the Environment

```bash
conda rename -n old_name new_name
```

Example:

```bash
conda rename -n infoscopy psair
```

---

### Step 4 — Verify Rename Worked

```bash
conda env list
```

Then test activation:

```bash
conda activate new_name
```

If activation works and packages behave as expected, rename is complete.

---

## Method 2 — Fallback for Older Conda Versions (< 4.14.0)

If `conda rename` is unavailable, use the clone/remove method.

### Step 1 — Clone the Environment

```bash
conda create --name new_name --clone old_name
```

Example:

```bash
conda create --name psair --clone infoscopy
```

---

### Step 2 — Test the New Environment

```bash
conda activate new_name
```

Verify:

- Python version
- Key packages
- CLI tools work

Optional check:

```bash
conda list
```

---

### Step 3 — Remove the Old Environment

Only after confirming the new one works:

```bash
conda remove --name old_name --all
```

---

## Common Gotchas

### 1. Trying to Rename While Active
Conda will refuse. Always `conda deactivate` first.

### 2. Renaming `base`
Not allowed. If you need a differently structured base-like environment, create a new one instead.

### 3. Editable Installs After Rename

If you previously ran:

```bash
pip install -e .
```

Inside the old environment, you may want to reinstall inside the renamed one:

```bash
pip uninstall <package>
pip install -e .
```

---

## When Should You Rename vs Recreate?

Rename is appropriate when:

- You want consistency across repos
- You are standardizing naming conventions (e.g., `infoscopy → psair`)
- The environment is stable and already validated

Recreate is often better when:

- The environment has dependency drift
- You are changing major Python versions
- You want a clean rebuild from `environment.yml`

---

## Micro-Template (Copy/Paste)

Deactivate:
```bash
conda deactivate
```

Verify:
```bash
conda env list
```

Rename (modern Conda):
```bash
conda rename -n old_name new_name
```

Fallback (older Conda):
```bash
conda create --name new_name --clone old_name
conda remove --name old_name --all
```

Verify:
```bash
conda activate new_name
conda list
```

---

## Final Checklist

- [ ] Not inside environment during rename  
- [ ] Confirmed Conda version  
- [ ] Verified old environment name  
- [ ] Rename or clone completed successfully  
- [ ] Activated new environment  
- [ ] Removed old environment (if using fallback)  
