# Contributing to Solo OS

Thanks for your interest in improving Solo OS.

## Before You Start

- Open an issue for significant changes before starting implementation.
- Keep changes scoped to one clear objective per pull request.
- Prefer additive improvements over broad rewrites unless a rewrite is explicitly justified.

## Local Development

```bash
git clone https://github.com/ScoopedOutStudios/solo-os.git
cd solo-os
pipx install -e .
python3 -m solo_os --help
```

## Submission Guidelines

- Describe the user-visible problem and expected behavior.
- Include validation notes (commands run, checks performed, and any manual smoke tests).
- Keep docs and command examples aligned with real CLI behavior.
- Avoid committing local secrets, machine-specific paths, or private internal references.

## Pull Request Checklist

- [ ] Scope is bounded and clearly described.
- [ ] Relevant docs are updated.
- [ ] CLI help/examples are accurate.
- [ ] Validation evidence is included in the PR description.
- [ ] No secrets or sensitive data are included.
