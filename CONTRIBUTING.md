# Contributing

Thank you for improving PM Review Copilot.

## What to change

- Keep each installable skill self-contained under `skills/`.
- Update both English and Chinese versions when behavior changes.
- Keep user-facing outputs in the language of the selected skill.
- Do not describe the skill as automatic, scheduled, or background-running.
- Keep review outputs focused on human decision points.

## Validation

Before opening a pull request or publishing a release:

```bash
python3 -m py_compile \
  skills/pm-review-copilot/scripts/*.py \
  skills/pm-review-copilot-zh/scripts/*.py

python3 skills/pm-review-copilot/scripts/init_pm_memory.py --path /tmp/pm-review-copilot-test-en --project-name "Test"
python3 skills/pm-review-copilot-zh/scripts/init_pm_memory.py --path /tmp/pm-review-copilot-test-zh --project-name "测试"
```

## Documentation

When README content changes, update all language files:

- `README.md`
- `docs/README.en.md`
- `docs/README.ja.md`
- `docs/README.ko.md`
