# Pigbibi/.github

Default community health files and repository hygiene baseline for `Pigbibi`
repositories.

## Contents

| Path | Purpose |
| --- | --- |
| `SECURITY.md` | Vulnerability reporting policy inherited by repositories |
| `CONTRIBUTING.md` | Contribution workflow and commit conventions |
| `CODE_OF_CONDUCT.md` | Community behavior standards |
| `.github/pull_request_template.md` | Default pull request checklist |
| `.github/ISSUE_TEMPLATE/` | Default issue forms |
| `scripts/check_hygiene.py` | Local documentation and leak-prevention check |

Reusable pull request governance actions live in
[Pigbibi/PrGovernance](https://github.com/Pigbibi/PrGovernance).

## Usage

```sh
python3 scripts/check_hygiene.py --strict
```

## License

Released under the [MIT License](LICENSE).
