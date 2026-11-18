# AGENTS.md

Rules for AI assistants and maintainers working in `Pigbibi/.github`.

## What this repository is

`Pigbibi/.github` provides default GitHub community health files and baseline
hygiene configuration for `Pigbibi` repositories.

## Stack

- Markdown community health and template files
- Python 3 (`scripts/check_hygiene.py`)
- GitHub Actions (`repository-hygiene.yml`)

## Layout

- `.github/` — default pull request template, issue templates, and CI workflow
- `actions/repository-hygiene/` — shared composite action wrapping `scripts/check_hygiene.py`
- `scripts/check_hygiene.py` — repository documentation and secret-hygiene checker
- Root files — `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`

## Local checks

```sh
python3 scripts/check_hygiene.py --strict
```

## Do not

- Do not duplicate `pr-governance/` here; reusable PR governance lives in
  `Pigbibi/PrGovernance`.
- Do not commit `docs/plans/`, `docs/audits/`, `docs/changes/`, or
  `docs/acceptance-policy.md`.
- Update `README.md` only for user-visible file or workflow changes, and keep
  all sections before `## License`.

- Set an explicit short `retention-days` (1-7 days) on `actions/upload-artifact`
  in private repositories to avoid exceeding the shared 500 MB storage quota.
- Keep personal/campus Cloudflare resources separated from `QuantStrategyLab` live
  trading edge accounts, and delete temporary smoke Workers after verification.

<!-- content-boundary:begin -->
- Use synthetic placeholders (`<owner>`, `<repo>`) instead of private IDs or
  real credentials.
- Judge whether a change is clean using `git diff` and `git ls-files`.
<!-- content-boundary:end -->

## Commits and pull requests

- Use English Conventional Commits with commit headers ≤ 72 characters.
- Branch from `origin/main` and fill in the standard PR template sections.
