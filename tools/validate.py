#!/usr/bin/env python3
"""Validate Absolut Skills plugin layout for Claude Code and Codex (stdlib only)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLUGIN_NAME = "as"
MARKETPLACE_NAME = "absolut-skills"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_KEYS = {
    "name",
    "description",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "argument-hint",
    "model",
}
MAX_DESCRIPTION = 1024
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKILL_MENTION_RE = re.compile(r"[$/]as:([a-z0-9-]+)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
FENCE_RE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.MULTILINE | re.DOTALL)
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")


def strip_fences(text: str) -> str:
    """Drop fenced code blocks: their links and headings are examples, not real targets."""
    return FENCE_RE.sub("", text)


def anchors(text: str) -> set[str]:
    """GitHub-style heading slugs plus explicit `<a id>` anchors of a Markdown text."""
    text = strip_fences(text)
    found = set(ANCHOR_RE.findall(text))
    for heading in HEADING_RE.findall(text):
        heading = ANCHOR_RE.sub("", heading).replace("`", "").strip().lower()
        found.add(re.sub(r"[^\w\- ]", "", heading).replace(" ", "-"))
    return found


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse simple `key: value` YAML frontmatter; returns None when absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line[0].isspace():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return None


def parse_simple_yaml(text: str) -> dict[str, dict[str, str]]:
    """Parse two-level `section:\n  key: value` YAML used by agents/openai.yaml."""
    data: dict[str, dict[str, str]] = {}
    section: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            section = line.split(":", 1)[0].strip()
            data[section] = {}
        elif section is not None and ":" in line:
            key, _, value = line.strip().partition(":")
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[section][key.strip()] = value
    return data


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
    return None


def check_manifests(root: Path, errors: list[str]) -> None:
    claude = load_json(root / ".claude-plugin/plugin.json", errors)
    codex = load_json(root / ".codex-plugin/plugin.json", errors)
    package = load_json(root / "package.json", errors)
    claude_mp = load_json(root / ".claude-plugin/marketplace.json", errors)
    codex_mp = load_json(root / ".agents/plugins/marketplace.json", errors)

    for label, manifest in ((".claude-plugin/plugin.json", claude), (".codex-plugin/plugin.json", codex)):
        if manifest is None:
            continue
        if manifest.get("name") != PLUGIN_NAME:
            errors.append(f"{label}: name must be {PLUGIN_NAME!r}")
        if not manifest.get("version"):
            errors.append(f"{label}: version is required")

    if codex is not None:
        if codex.get("skills") != "./skills/":
            errors.append(".codex-plugin/plugin.json: skills must be './skills/'")
        if not isinstance(codex.get("interface"), dict) or not codex["interface"].get("displayName"):
            errors.append(".codex-plugin/plugin.json: interface.displayName is required")

    versions = {}
    if claude:
        versions[".claude-plugin/plugin.json"] = str(claude.get("version", ""))
    if codex:
        versions[".codex-plugin/plugin.json"] = str(codex.get("version", "")).split("+", 1)[0]
    if package:
        versions["package.json"] = str(package.get("version", ""))
    if len(set(versions.values())) > 1:
        errors.append(f"version mismatch: {versions}")

    for label, mp in ((".claude-plugin/marketplace.json", claude_mp), (".agents/plugins/marketplace.json", codex_mp)):
        if mp is None:
            continue
        if mp.get("name") != MARKETPLACE_NAME:
            errors.append(f"{label}: name must be {MARKETPLACE_NAME!r}")
        names = [p.get("name") for p in mp.get("plugins", []) if isinstance(p, dict)]
        if PLUGIN_NAME not in names:
            errors.append(f"{label}: must list plugin {PLUGIN_NAME!r}")


def check_links(path: Path, text: str, errors: list[str]) -> None:
    for target in LINK_RE.findall(CODE_SPAN_RE.sub("", strip_fences(text))):
        if re.match(r"^[a-z]+:", target):
            continue
        rel, _, fragment = target.partition("#")
        dest = path.parent / rel if rel else path
        if not dest.exists():
            errors.append(f"{path}: broken link {target!r}")
        elif fragment and dest.suffix == ".md" and fragment not in anchors(dest.read_text(encoding="utf-8")):
            errors.append(f"{path}: broken anchor {target!r}")


def check_skills(root: Path, errors: list[str]) -> None:
    skills_dir = root / "skills"
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    if not skill_dirs:
        errors.append("skills/: no skills found")
    known = {p.name for p in skill_dirs}

    for skill in skill_dirs:
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None:
            errors.append(f"{skill_md}: missing or unterminated frontmatter")
            continue
        unknown = set(meta) - SKILL_KEYS
        if unknown:
            errors.append(f"{skill_md}: unknown frontmatter keys {sorted(unknown)}")
        name = meta.get("name", "")
        if name != skill.name:
            errors.append(f"{skill_md}: name {name!r} must equal directory name {skill.name!r}")
        if not SKILL_NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{skill_md}: name {name!r} must be lowercase kebab-case, max 64 chars")
        description = meta.get("description", "")
        if not description:
            errors.append(f"{skill_md}: description is required")
        elif len(description) > MAX_DESCRIPTION:
            errors.append(f"{skill_md}: description longer than {MAX_DESCRIPTION} chars")
        for key in ("disable-model-invocation", "user-invocable"):
            if key in meta and meta[key] not in ("true", "false"):
                errors.append(f"{skill_md}: {key} must be true or false")
        check_links(skill_md, text, errors)

        openai = skill / "agents/openai.yaml"
        if not openai.is_file():
            errors.append(f"{skill}: missing agents/openai.yaml")
            continue
        yaml_text = openai.read_text(encoding="utf-8")
        yaml = parse_simple_yaml(yaml_text)
        interface = yaml.get("interface", {})
        for key in ("display_name", "short_description"):
            if not interface.get(key):
                errors.append(f"{openai}: interface.{key} is required")
        implicit = yaml.get("policy", {}).get("allow_implicit_invocation", "true")
        if (meta.get("disable-model-invocation") == "true") != (implicit == "false"):
            errors.append(
                f"{skill}: disable-model-invocation: true in SKILL.md requires "
                "policy.allow_implicit_invocation: false in agents/openai.yaml, and vice versa"
            )
        for mentioned in SKILL_MENTION_RE.findall(yaml_text):
            if mentioned not in known:
                errors.append(f"{openai}: references unknown skill 'as:{mentioned}'")

    docs = [root / "README.md", skills_dir / "README.md", *sorted((root / "references").glob("*.md"))]
    docs += sorted(skills_dir.glob("*/references/*.md"))
    for doc in docs:
        if doc.is_file():
            check_links(doc, doc.read_text(encoding="utf-8"), errors)

    if (root / "commands").exists():
        errors.append("commands/: not supported by Codex; use skills/ instead")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    check_manifests(root, errors)
    check_skills(root, errors)
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors = validate(root)
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"{len(errors)} error(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
