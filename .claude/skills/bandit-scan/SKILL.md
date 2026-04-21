---
name: bandit-scan
description: Use when the user asks to run a Bandit security scan on a Python package, audit a Python codebase for security issues, or review/triage Bandit findings. Runs Bandit with the package's bandit.yaml, triages findings by severity, proposes remediations, and verifies tests still pass.
---

# Bandit security scan

Run Bandit against a Python package, triage each finding with real-world risk
analysis, propose remediations, and verify the test suite still passes after fixes.

## Step 1 — Verify Bandit is installed

Run:

```bash
bandit --version
```

- If the command fails or is not found, STOP and report to the user:
  "Bandit is not installed. Install it with `pip install bandit` (or the project's
  preferred installer, e.g. `uv pip install bandit` inside the venv) and re-run."
- Do NOT attempt to install Bandit yourself.

## Step 2 — Locate the Bandit config and source root

Find the Bandit config file:

```bash
# From the project or package root
ls bandit.yaml .bandit.yaml 2>/dev/null
```

If none is found, ask the user where the config lives (or whether to run without
a config file, using Bandit defaults).

Determine the source root to scan. Common layouts:

- `src/<package>/` (src-layout) → scan `src/<package>`
- `<package>/` at repo root (flat-layout) → scan `<package>`

If ambiguous, ask the user which path to scan. Do NOT scan the entire repo
unless asked — it pulls in vendored dependencies, build artifacts, and tests.

## Step 3 — Run Bandit

Run from the directory containing `bandit.yaml`:

```bash
bandit -r <source-root> -c bandit.yaml -f json -o /tmp/bandit-report.json
```

Then read `/tmp/bandit-report.json`. If Bandit exits non-zero for reasons other than
findings (config error, parse failure), surface the error and stop.

## Step 4 — Analyze findings

Parse `results[]` from the JSON. For each finding, extract:

- `issue_severity` (HIGH / MEDIUM / LOW)
- `issue_confidence`
- `test_id` and `test_name`
- `filename` and `line_number`
- `issue_text`
- `code` (the offending snippet)

**Sort findings by severity: HIGH → MEDIUM → LOW.** Within the same severity, sort by
confidence (HIGH → MEDIUM → LOW), then by filename.

If there are zero findings, report that and stop.

## Step 5 — For each finding, produce an analysis

Present findings one at a time, in sorted order. For each finding, write:

### `<severity>` — `<test_id>` `<test_name>` — `<file>:<line>`

**What Bandit flagged:**
One-sentence summary of the offending code.

**Actual risk in this codebase:**
Explain the *real-world* impact given how this code is used. Read the surrounding
code and call sites before answering. Distinguish between:
- Real exploitable risk (e.g. user-controlled input reaching the sink)
- Theoretical risk (the pattern is risky but inputs are trusted/internal)
- False positive (the pattern is safe in context)

Do not copy Bandit's generic description — assess *this* occurrence.

**Proposed remediation:**
Concrete code change. Show a before/after diff when helpful. If the right fix is
`# nosec BXXX` with a justifying comment (false positive or accepted risk),
say so explicitly and justify it.

**Test impact:**
Identify tests that exercise the affected code path (grep the test suite for the
module/function name). List them. If none exist, say so.

## Step 6 — Apply remediations

After the user approves a remediation (or a batch), apply the change, then run the
project's test suite to confirm nothing breaks.

Discover the project's test command from (in order):
- `Makefile` targets (`make test`, `make check`)
- `pyproject.toml` / `setup.cfg` / `tox.ini` (pytest, tox, zope.testrunner config)
- `CLAUDE.md` or `README` in the repo
- Conventional entry points (`bin/test`, `pytest`, `python -m pytest`)

If unclear, ask the user for the correct command before running anything.

Run the most targeted invocation first (single test file or matching name), then
widen to the affected module's full suite.

Do NOT mark a finding resolved until its associated tests pass. If a fix breaks
tests, revert it and re-analyze — the remediation is wrong, not the test.

## Step 7 — Re-run Bandit

After all approved remediations are applied, re-run Step 3 and confirm the
finding count dropped as expected. Report the diff (fixed / remaining / newly
introduced).
