import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIEWER = (ROOT / "skills/feature/assets/mockups.html").read_text(encoding="utf-8")
RULES = (ROOT / "skills/feature/references/mockups.md").read_text(encoding="utf-8")


def test_viewer_reads_every_key_of_the_documented_tabs_js():
    example = re.search(r"```js\n(.*?)```", RULES, re.S).group(1)
    assert "window.MOCKUPS = {" in example and "window.MOCKUPS" in VIEWER
    assert '<script src="tabs.js">' in VIEWER
    keys = set(re.findall(r'(?:^\s*|\{ |", )(\w+): ', example, re.M))
    assert keys == {"title", "tabs", "id", "label", "file", "note"}
    for key in keys - {"title", "tabs"}:
        assert f"tab.{key}" in VIEWER, key
    assert "data.title" in VIEWER and "data.tabs" in VIEWER


def test_every_documented_tab_names_a_file_of_the_example_tree():
    tree = re.search(r"```text\n(.*?)```", RULES, re.S).group(1)
    example = re.search(r"```js\n(.*?)```", RULES, re.S).group(1)
    files = re.findall(r'file: "([^"]+)"', example)
    assert files and all(name in tree for name in files)
