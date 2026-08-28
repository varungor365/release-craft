# release-craft: Dry-Run Release Notes from Git History

**Turn git history into honest, user-facing release notes without creating a release.**

`release-craft` groups conventional commits and ordinary commit subjects into readable Markdown or JSON release drafts. It filters obvious merge noise, keeps original commit text available for review, and never creates tags, releases, or claims that are not present in the history.

## Why this exists

Release notes are part of the software interface, but writing them from raw history is repetitive and easy to make misleading. `release-craft` provides a provider-neutral draft that a maintainer can inspect, edit, and publish through an existing release process.

| Use case | What to run |
|---|---|
| Draft notes between tags | `release_craft --from v0.3.0 --to HEAD` |
| Review in automation | `release_craft --from v0.3.0 --to HEAD --format json` |
| Convert an existing subject list | `release_craft --input commits.txt --output RELEASE_NOTES.md` |
| Preview without side effects | Use the default dry-run output and review before publishing |

## Three-minute quick start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install release-craft
release_craft --from v0.3.0 --to HEAD
```

To save a machine-readable draft or process a prepared list:

```bash
release_craft --from v0.3.0 --to HEAD --format json > release.json
release_craft --input commits.txt --output RELEASE_NOTES.md
```

The generator is intentionally a draft assistant. Review the output, add migration notes when needed, then publish through your normal release process. GitHub's [generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) remain a useful baseline; this tool is for local preview and more readable grouping.

## Categories

Features, fixes, performance, documentation, maintenance, and other changes are grouped from conventional commit prefixes. Breaking changes are called out when a commit uses `!` or includes `BREAKING CHANGE`. Merge and Dependabot noise is filtered when it matches the tool's built-in patterns.

## Safe defaults and honest limitations

`release-craft` reads git history or an input file and writes a draft. It does not create tags, publish GitHub Releases, call a hosting provider, infer undocumented behavior, or guarantee that a commit subject is user-facing. Non-conventional or vague subjects may land in a generic category and still need editorial review. If a requested git range is unavailable, fix the range or use `--input` with an explicit subject list.

## Why star this repository?

Star this project if you maintain a library or CLI, want repeatable release drafts from git history, or need a local and provider-neutral alternative to writing changelogs from scratch.

## Development

```bash
git clone https://github.com/varungor365/release-craft
cd release-craft
python -m pip install -e '.[dev]'
pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
