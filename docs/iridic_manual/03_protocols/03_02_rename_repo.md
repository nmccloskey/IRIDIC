# Rename a GitHub Repo (and keep VS Code + remotes + PyPI happy)

This is a **practical, copy/paste playbook** for renaming a repository while keeping:
- GitHub redirects and URLs sane
- your local clone’s `origin` correct
- VS Code happy on Windows
- (optionally) your **Python distribution name** and **import package name** consistent for PyPI

Assumptions: **Windows + VS Code + repo already cloned locally**.

---

## 0. Decide what is being renamed

You may be renaming **up to three different things** (they can match, but they don’t have to):

1. **GitHub repository name** (affects URL and remote):  
   `Infoscopy → PSAIR`
2. **Local folder name** (what you see on disk / in VS Code):  
   `...\GitRepos\Infoscopy → ...\GitRepos\PSAIR`
3. **Python names** (only relevant if publishing / packaging):
   - **PyPI distribution name** (what `pip install ...` uses): e.g. `psair`
   - **Python import package** (what `import ...` uses): e.g. `psair` (must be a valid identifier)

If you’re doing a “minimal PyPI upload,” (3) matters even if (2) is optional.

---

## 1. Rename on GitHub

1. Go to your repo on GitHub
2. **Settings → Repository name → Rename**
3. GitHub usually sets up **redirects** from old URLs to new ones (handy, but don’t rely on it forever).

---

## 2. Update your local git remote (origin) to the new GitHub URL

From a terminal **inside the repo** (VS Code Terminal is fine):

```bash
git remote -v
git remote set-url origin https://github.com/<YOUR_USER_OR_ORG>/PSAIR.git
git remote -v
git fetch
```

### Alternate (same outcome): remove + re-add origin

```bash
git remote remove origin
git remote add origin https://github.com/<YOUR_USER_OR_ORG>/PSAIR.git
git fetch
```

### Quick sanity checks

```bash
git status
git branch -vv
git remote show origin
```

If you see the new URL and `git fetch` works, you’re good.

---

## 3. Rename the local folder (optional but recommended on Windows)

This is not required for Git correctness, but it reduces cognitive friction.

**Best practice on Windows with VS Code**:

1. **Close VS Code** (important: reduces file-lock weirdness)
2. Rename the folder in File Explorer:
   - `...\GitRepos\Infoscopy` → `...\GitRepos\PSAIR`
3. Reopen VS Code via **File → Open Folder…** and select the new folder.

### If you use a VS Code Workspace (.code-workspace)

Update the folder path inside it, or recreate the workspace.

---

## 4. If your Python package name changes, update the codebase (PyPI-relevant)

This is the part that actually matters for packaging.

### 4.1 Update project metadata (pyproject.toml)

At minimum, verify/update:

- `name = "psair"` (PyPI distribution name)
- `version = "0.0.1a1"` (or current)
- `description`, `readme`, `license`, `authors`
- `urls` / `Homepage` / `Repository` → point to the new GitHub URL

Also ensure your build backend and package discovery are correct:
- `hatchling` / `setuptools` / `poetry` etc.
- `src/` layout vs flat layout

**Example URLs block** (adjust to your schema/backend):

```toml
[project.urls]
Homepage = "https://github.com/<YOUR_USER_OR_ORG>/PSAIR"
Repository = "https://github.com/<YOUR_USER_OR_ORG>/PSAIR"
Issues = "https://github.com/<YOUR_USER_OR_ORG>/PSAIR/issues"
```

### 4.2 Rename the import package (if applicable)

If you currently do `import infoscopy` and you want `import psair`:

1. Rename the top-level package folder:
   - `src/infoscopy/` → `src/psair/`  
   *(or `infoscopy/` → `psair/` if you’re not using `src/`)*

2. Update imports across the repo:
   - `from infoscopy...` → `from psair...`
   - `import infoscopy` → `import psair`

3. Update tests and docs similarly.

**VS Code fast replace**:
- `Ctrl + Shift + F` → search `infoscopy` → replace carefully

> Tip: Do a first pass replacing **imports** before changing any human-facing prose. It reduces accidental breakage.

### 4.3 Update CLI entry point (if you have one)

If you expose a console script, update it in `pyproject.toml`, e.g.:

```toml
[project.scripts]
psair = "psair.cli:main"
```

Make sure `psair/cli.py` exists and defines `main()`.

---

## 5. Update README, badges, and internal links

Minimum set:

- README title, install snippet: `pip install psair`
- GitHub Actions badge URLs (often include repo name)
- Any hardcoded old GitHub URLs in docs
- `CITATION.cff` `repository-code` (if present)
- `CONTRIBUTING.md`, `SECURITY.md`, docs site configs, etc.

**Find likely stale links**:

```bash
git grep -n "Infoscopy"
git grep -n "infoscopy"
git grep -n "github.com/.*/Infoscopy"
```

---

## 6. Minimal PyPI upload checklist (don’t get blocked)

From repo root:

### Build

```bash
python -m build
```

### Validate dist artifacts

```bash
python -m twine check dist/*
```

### Upload to TestPyPI (recommended even for “minimal”)

```bash
python -m twine upload -r testpypi dist/*
```

### Install from TestPyPI to confirm

```bash
python -m pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple psair
```

### Upload to real PyPI

```bash
python -m twine upload dist/*
```

---

## 7. Common gotchas

- **Repo renamed but remote not updated** → `git push` tries old URL and fails.
- **Distribution name vs import name confusion**
  - `pip install psair` should ideally give you `import psair`.
- **Leftover references**
  - Especially in `__init__.py`, docs, tests, badges, and config files.
- **Editable install confusion**
  - If you previously ran `pip install -e .`, reinstall after renaming the package folder:
    ```bash
    python -m pip uninstall -y infoscopy psair
    python -m pip install -e .
    ```

---

## 8. Compact “IRIDIC-able” micro-template (copy/paste)

**Rename GitHub repo**
- GitHub Settings → Rename
- Update local remote:
  ```bash
  git remote set-url origin <new_url>
  git fetch
  ```

**Rename local folder**
- Close VS Code → rename folder → reopen folder

**Rename Python package (optional)**
- Update `pyproject.toml` name + URLs
- Rename `src/<oldpkg>` → `src/<newpkg>`
- Replace imports `<oldpkg>` → `<newpkg>`

**Build & upload**
- `python -m build`
- `python -m twine check dist/*`
- Upload TestPyPI → install test → upload PyPI

---

## 9. Quick “did I finish?” checklist

- [ ] GitHub repo renamed; new URL works  
- [ ] `git remote -v` shows new origin URL  
- [ ] `git fetch` works  
- [ ] (Optional) local folder renamed; VS Code opens new folder cleanly  
- [ ] `pyproject.toml` name/urls updated (if packaging)  
- [ ] imports updated and tests pass (if package renamed)  
- [ ] README/badges/links updated  
- [ ] build passes; `twine check` passes  
