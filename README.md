# release-craft

**Turn git history into honest, user-facing release notes in a dry run.**

`release-craft` groups conventional commits and ordinary commit subjects into readable Markdown or JSON release drafts. It filters obvious merge noise, keeps the original commit text available for review, and never creates tags, releases, or claims that are not present in the history.

## Quick start

```bash
pipx install release-craft
release-craft --from v0.3.0 --to HEAD
release-craft --from v0.3.0 --to HEAD --format json > release.json
release-craft --input commits.txt --output RELEASE_NOTES.md
```

The generator is intentionally a draft assistant. Review the output, add migration notes when needed, then publish through your normal release process. GitHub’s own generated release notes remain a useful baseline; this tool is for local preview and more readable grouping.

## Categories

Features, fixes, performance, documentation, maintenance, and other changes are grouped from conventional commit prefixes. Breaking changes are called out when a commit uses `!` or includes `BREAKING CHANGE`.

## Why star this repository

Star this project if you maintain a library or CLI, want repeatable release drafts from git history, or need a local and provider-neutral alternative to writing changelogs from scratch.

## Development

```bash
git clone https://github.com/varungor365/release-craft
cd release-craft
python -m pip install -e ".[dev]"
pytest -q
```

## License

MIT.
