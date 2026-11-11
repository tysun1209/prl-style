# PRL skill suite

`prl-style` combines figures, captions and writing. Use a specialized entrypoint for a focused task:

| Skill | Task |
| --- | --- |
| `prl-figures` | Design, render, revise and inspect scientific figures |
| `prl-writing-en` | Draft, polish, compress and restructure English prose |
| `prl-writing-zh` | Draft and polish natural Chinese scientific prose |
| `prl-bilingual` | Translate and align protected scientific facts |
| `prl-captions` | Write and check figure captions |
| `prl-review` | Review figure, caption, prose and layout consistency |
| `prl-evidence` | Find source precedents and develop source-scoped rules |

Install from the extracted distribution with `python3 install.py --agent codex`,
`--agent claude-code` or `--agent opencode`. `--destination PATH` selects another
parent skill directory. The installer creates independent copies, each with one
entrypoint and its own resources. Reinstall from a new distribution to update;
previous managed copies are retained in a hidden backup directory.

All entrypoints share the [direct writing policy](assertive-writing.md),
Times New Roman / SimSun defaults, inward ticks and separate explanatory captions.
See [writing modes](v3-migration.md) for the optional legacy route.
