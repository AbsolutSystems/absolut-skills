import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from validate import validate  # noqa: E402


def copy_repo(tmp_path: Path) -> Path:
    dest = tmp_path / "repo"
    shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache"))
    return dest


def test_repository_is_valid():
    assert validate(ROOT) == []


def test_skill_name_must_match_directory(tmp_path):
    repo = copy_repo(tmp_path)
    skill = repo / "skills/help/SKILL.md"
    skill.write_text(skill.read_text().replace("name: help", "name: other"))
    assert any("must equal directory name" in e for e in validate(repo))


def test_missing_description_and_unknown_key(tmp_path):
    repo = copy_repo(tmp_path)
    (repo / "skills/broken/agents").mkdir(parents=True)
    (repo / "skills/broken/SKILL.md").write_text("---\nname: broken\nfoo: bar\n---\nBody\n")
    (repo / "skills/broken/agents/openai.yaml").write_text('interface:\n  display_name: "B"\n  short_description: "B"\n')
    errors = validate(repo)
    assert any("description is required" in e for e in errors)
    assert any("unknown frontmatter keys" in e for e in errors)


def test_missing_openai_yaml(tmp_path):
    repo = copy_repo(tmp_path)
    (repo / "skills/help/agents/openai.yaml").unlink()
    assert any("missing agents/openai.yaml" in e for e in validate(repo))


def test_version_mismatch(tmp_path):
    repo = copy_repo(tmp_path)
    path = repo / ".codex-plugin/plugin.json"
    data = json.loads(path.read_text())
    data["version"] = "9.9.9"
    path.write_text(json.dumps(data))
    assert any("version mismatch" in e for e in validate(repo))


def test_codex_build_suffix_is_allowed(tmp_path):
    repo = copy_repo(tmp_path)
    path = repo / ".codex-plugin/plugin.json"
    data = json.loads(path.read_text())
    data["version"] = data["version"] + "+codex.1"
    path.write_text(json.dumps(data))
    assert validate(repo) == []


def test_plugin_name_must_be_as(tmp_path):
    repo = copy_repo(tmp_path)
    path = repo / ".claude-plugin/plugin.json"
    data = json.loads(path.read_text())
    data["name"] = "absolut-skills"
    path.write_text(json.dumps(data))
    assert any("name must be 'as'" in e for e in validate(repo))
