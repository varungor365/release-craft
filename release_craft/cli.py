from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

PREFIXES = {"feat": "Features", "fix": "Fixes", "perf": "Performance", "docs": "Documentation", "refactor": "Maintenance", "test": "Tests", "build": "Maintenance", "ci": "Maintenance", "chore": "Maintenance"}
CONVENTIONAL = re.compile(r"^(?P<type>[a-z]+)(?:\([^)]*\))?(?P<breaking>!)?:\s*(?P<subject>.+)$")


@dataclass
class Commit:
    subject: str
    category: str
    breaking: bool


def classify(subject: str) -> Commit:
    match = CONVENTIONAL.match(subject.strip())
    if match:
        kind = match.group("type")
        title = match.group("subject").strip()
        category = PREFIXES.get(kind, "Other")
        breaking = bool(match.group("breaking")) or "BREAKING CHANGE" in subject.upper()
        return Commit(title, category, breaking)
    return Commit(subject.strip(), "Other", "BREAKING CHANGE" in subject.upper())


def filter_subjects(subjects: list[str]) -> list[str]:
    return [subject.strip() for subject in subjects if subject.strip() and not subject.lower().startswith(("merge ", "dependabot", "bump "))]


def render(commits: list[Commit], title: str = "Release draft") -> str:
    groups: dict[str, list[str]] = {}
    breaking = [commit.subject for commit in commits if commit.breaking]
    for commit in commits:
        groups.setdefault(commit.category, []).append(commit.subject)
    lines = [f"# {title}", ""]
    if breaking:
        lines += ["## Breaking changes", ""] + [f"- {subject}" for subject in breaking] + [""]
    order = ["Features", "Fixes", "Performance", "Documentation", "Maintenance", "Tests", "Other"]
    for category in order:
        if category in groups:
            lines += [f"## {category}", ""] + [f"- {subject}" for subject in groups[category]] + [""]
    return "\n".join(lines).rstrip() + "\n"


def git_subjects(old: str | None, new: str) -> list[str]:
    revision = f"{old}..{new}" if old else new
    result = subprocess.run(["git", "log", revision, "--format=%s"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git log failed")
    return filter_subjects(result.stdout.splitlines())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a dry-run release draft from git history")
    parser.add_argument("--from", dest="old")
    parser.add_argument("--to", dest="new", default="HEAD")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    subjects = filter_subjects(args.input.read_text(encoding="utf-8").splitlines()) if args.input else git_subjects(args.old, args.new)
    commits = [classify(subject) for subject in subjects]
    if args.format == "json":
        output = json.dumps({"commits": [asdict(commit) for commit in commits]}, indent=2) + "\n"
    else:
        output = render(commits)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
