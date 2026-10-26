import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/health/scripts"))
sys.path.insert(0, str(ROOT / "skills/spec-docs/scripts"))
sys.path.insert(0, str(ROOT / "skills/estimate/scripts"))

from estimate_totals import check, totals  # noqa: E402
from git_signals import signals  # noqa: E402
from spec_lint import lint  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_git_signals_coupling_fixed_tests_and_large_commits():
    history = [("feat", {"a/x.py": 3, "b/y.py": 1})] * 5
    history += [("fix flaky", {"a/test_x.py": 2})] * 2
    history += [("format", {f: 0 for f in [f"f{i}.py" for i in range(31)] + ["a/x.py", "b/y.py"]})]
    history += [("lock", {"package-lock.json": 9, "docs/z.md": 9})]
    result = signals(history, ["docs/*", "*lock.json"], max_files=30)
    assert result["coupling"] == [{"a": "a/x.py", "b": "b/y.py", "shared": 5, "confidence": 0.83}]
    assert result["frequently_fixed_tests"] == [{"file": "a/test_x.py", "fix_commits": 2}]
    assert result["skipped_large_commits"] == 1
    assert result["churn"][0] == {"file": "a/x.py", "commits": 6, "lines": 15}
    assert not any(c["file"] in ("package-lock.json", "docs/z.md") for c in result["churn"])


MODULE = """<!-- as:spec-docs lang=en -->
# Orders

[Billing](billing.md#BIL-001)

### <a id="ORD-R1"></a>ORD-R1 — Place

#### <a id="ORD-001"></a>ORD-001 — Place an order
"""

PROPOSAL = """<!-- as:tech-lead lang=en -->
# Cancel

#### <a id="ORD-002"></a>ORD-002 — Cancel

**Kind:** ✅ happy · **Change:** 🆕 added

#### <a id="ORD-001"></a>ORD-001 — Place an order

**Kind:** ✅ happy · **Change:** ✏️ changed
"""


def spec(tmp_path: Path) -> Path:
    root = tmp_path / "docs/spec"
    write(root / "orders.md", MODULE)
    write(root / "billing.md", '# Billing\n\n#### <a id="BIL-001"></a>BIL-001 — Refund\n')
    write(root / "changes/cancel.md", PROPOSAL)
    return root


def test_spec_lint_clean(tmp_path):
    assert lint(spec(tmp_path)) == []


def test_spec_lint_duplicates_html_and_links(tmp_path):
    root = spec(tmp_path)
    write(root / "billing.md", '# Billing\n\n<b>x</b> <https://ok.example>\n\n#### <a id="ORD-001"></a>ORD-001 — Dup\n')
    write(root / "changes/other.md", PROPOSAL.replace("ORD-001", "ORD-009"))
    write(root / "old.html", "<html></html>")
    errors = "\n".join(lint(root))
    assert "legacy HTML page" in errors
    assert "billing.md:3: raw HTML" in errors and "ok.example" not in errors
    assert "duplicate ID 'ORD-001'" in errors
    assert "ID 'ORD-002' added by several open proposals" in errors
    assert "broken anchor 'billing.md#BIL-001'" in errors


def test_spec_lint_against_ref_finds_id_taken_on_other_branch(tmp_path):
    root = spec(tmp_path)
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "base")
    git(tmp_path, "checkout", "-qb", "other")
    write(root / "orders.md", MODULE + '\n#### <a id="ORD-002"></a>ORD-002 — Taken elsewhere\n')
    git(tmp_path, "commit", "-qam", "other")
    git(tmp_path, "checkout", "-q", "main")
    import os

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        errors = lint(Path("docs/spec"), "other")
    finally:
        os.chdir(cwd)
    assert errors == ["docs/spec/changes/cancel.md: added ID 'ORD-002' already used on other"]


ANALYSIS = """# Cancel items

## Estimate

| Step | Block | Min | Likely | Max |
|------|-------|-----|--------|-----|
| 1.1 Cancel operation | Item cancellation | 2 | 3 | 6 |
| 1.2 Refund | Item cancellation | 1 | 2 | 3 |
| 2.1 Questions, demo | Communication | 1,1 | 1,5 | 2 |

Second table after text:

| Step | Block | Min | Likely | Max |
|------|-------|-----|--------|-----|
| 2.2 Docs | Communication | 2.2 | 2.2 | 2.2 |

## Optional additions

| Step | Block | Min | Likely | Max |
|------|-------|-----|--------|-----|
| O1 Email to customer | Cancellation email | 1 | 2 | 4 |
"""

CLIENT = """| Zakres | Godziny | Oczekiwane |
|--------|---------|------------|
| Item cancellation | 3–9 h | 5,5 h |
| **Communication** | 3,3–4,2 h | 4 h |
| **Razem** | 6,3–13,2 h | 9,5 h |

| Opcja | Godziny | Oczekiwane |
|-------|---------|------------|
| Cancellation email | 1–4 h | 2,5 h |
"""

CLIENT_TEXT_NUMBERS = """| Zakres | Opis | Godziny | Oczekiwane |
|--------|------|---------|------------|
| Item cancellation | 3 or 9 h, 5.5 h | 1–2 h | 1 h |
| Communication | | 3,3–4,2 h | 4 h |
| Cancellation email | | 1–4 h | 2,5 h |
"""


def test_estimate_totals_blocks_options_and_pert():
    result, errors = totals(ANALYSIS)
    assert errors == []
    assert result["blocks"] == [
        {"block": "Item cancellation", "min": 3, "likely": 5, "max": 9, "expected": 5.5},
        {"block": "Communication", "min": 3.3, "likely": 3.7, "max": 4.2, "expected": 4},
    ]
    assert result["options"] == [{"block": "Cancellation email", "min": 1, "likely": 2, "max": 4, "expected": 2.5}]
    assert result["total"] == {"min": 6.3, "likely": 8.7, "max": 13.2, "expected": 9.5}
    assert check(result, CLIENT) == []


def test_estimate_totals_reports_bad_rows_and_client_mismatch():
    _, errors = totals(ANALYSIS.replace("| 2 | 3 | 6 |", "| 4 | 3 | x |"))
    assert errors == ["step '1.1 Cancel operation': min, likely and max must be numbers"]
    _, errors = totals(ANALYSIS.replace("| 2 | 3 | 6 |", "| 4 | 3 | 6 |"))
    assert errors == ["step '1.1 Cancel operation': expected min <= likely <= max"]
    result, _ = totals(ANALYSIS)
    errors = check(result, CLIENT.replace("5,5 h", "5 h").replace("| Cancellation email", "| Email"))
    assert errors == [
        "client.md: block 'Item cancellation' should show 3–9 h, expected 5.5 h",
        "client.md: no table row for block 'Cancellation email'",
    ]
    errors = check(result, CLIENT_TEXT_NUMBERS)
    assert errors == [
        "client.md: block 'Item cancellation' should show 3–9 h, expected 5.5 h",
        "client.md: no total row showing 6.3–13.2 h, expected 9.5 h",
    ]
