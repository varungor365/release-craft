from release_craft.cli import classify, filter_subjects, render


def test_classify_conventional_commit():
    commit = classify("feat(api)!: add cursor pagination")
    assert commit.category == "Features"
    assert commit.breaking is True
    assert commit.subject == "add cursor pagination"


def test_filter_removes_noise():
    assert filter_subjects(["Merge branch main", "fix: close leak", "dependabot: bump x"]) == ["fix: close leak"]


def test_render_groups_changes():
    output = render([classify("feat: add export"), classify("fix: handle empty input")])
    assert "## Features" in output
    assert "## Fixes" in output
