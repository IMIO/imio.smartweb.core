---
name: bandit-scan
description: Use when the user asks to run a Bandit security scan on a Python package, audit a Python codebase for security issues, or review/triage Bandit findings. Triages findings by severity, proposes remediations, and verifies tests still pass.
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

Bandit reads configuration from several sources. Probe them in this order:

```bash
# 1. Explicit YAML config files (passed via -c)
ls bandit.yaml .bandit.yaml 2>/dev/null

# 2. INI-style .bandit file (passed via --ini)
ls .bandit 2>/dev/null

# 3. setup.cfg with [bandit] section (auto-read by Bandit)
grep -l '\[bandit\]' setup.cfg 2>/dev/null

# 4. pyproject.toml with [tool.bandit] section (auto-read by Bandit)
grep -l 'tool\.bandit' pyproject.toml 2>/dev/null
```

**Config precedence and flags:**

| Config file | CLI flag | Auto-discovered? |
|---|---|---|
| `bandit.yaml` / `.bandit.yaml` | `-c <file>` | No — must pass explicitly |
| `.bandit` (INI format) | `--ini <file>` | No — must pass explicitly |
| `setup.cfg` `[bandit]` | — | Yes — Bandit reads automatically |
| `pyproject.toml` `[tool.bandit]` | — | Yes — Bandit reads automatically |
| None found | — | Run with Bandit defaults |

If multiple configs exist, tell the user which one(s) were found and which will be used.
If none is found, ask the user whether to run with Bandit defaults or provide a config path.

Determine the source root to scan. Common layouts:

- `src/<package>/` (src-layout) → scan `src/<package>`
- `<package>/` at repo root (flat-layout) → scan `<package>`

If ambiguous, ask the user which path to scan. Do NOT scan the entire repo
unless asked — it pulls in vendored dependencies, build artifacts, and tests.

## Step 3 — Run Bandit

Run from the project root. Choose the command based on what config was found in Step 2:

```bash
# With an explicit YAML config (-c):
bandit -r <source-root> -c bandit.yaml -f json -o /tmp/bandit-report.json

# With an INI .bandit file (--ini):
bandit -r <source-root> --ini .bandit -f json -o /tmp/bandit-report.json

# With setup.cfg [bandit] or pyproject.toml [tool.bandit] (auto-read, no extra flag):
bandit -r <source-root> -f json -o /tmp/bandit-report.json

# With no config (Bandit defaults):
bandit -r <source-root> -f json -o /tmp/bandit-report.json
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
