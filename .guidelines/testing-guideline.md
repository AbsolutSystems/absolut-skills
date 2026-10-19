# Testing guideline

How to verify changes: the validator and its tests, and manual checks of skill output.

## Rules

- After every change run `python3 tools/validate.py`; it must print `OK`.
- Changing `tools/validate.py`: add or adjust a test in `tests/test_validate.py` and run
  `uv run --with pytest pytest tests`. Tests copy the repository to `tmp_path` (`copy_repo`) and break one thing, then
  assert on the error message; `test_repository_is_valid` must stay green.
- The validator stays standard-library only (no dependencies).
- Optionally run `claude plugin validate .`; the root `CLAUDE.md` warning is expected.
- Changing `spec.css` or an HTML skeleton: render the skeleton from the reference file with `spec.css` in a browser
  (light mode at least) and check labels do not overlap; serve from a temporary directory, not the repository.
- Changing a procedure: dry-run it on a sample repository when possible and state in the change what was not run.

## Reference examples

- `tests/test_validate.py` — `test_skill_name_must_match_directory` (copy, break, assert pattern).
