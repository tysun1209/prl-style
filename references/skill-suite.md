# PRL skill suite

`prl-style` combines figures, captions and writing. Use a specialized entrypoint for a focused task:

| Skill | Task |
| --- | --- |
| `prl-figures` | Design, render, revise and inspect scientific figures |
| `prl-schematics` | Generate scientific Fig. 1 PNGs with the host image model, then reconstruct editable PowerPoint diagrams |
| `prl-writing-en` | Draft, polish, compress and restructure English prose |
| `prl-writing-zh` | Draft and polish natural Chinese scientific prose |
| `prl-bilingual` | Translate and align protected scientific facts |
| `prl-captions` | Write and check figure captions |
| `prl-review` | Review figure, caption, prose and layout consistency |
| `prl-evidence` | Find source precedents and develop source-scoped rules |

Install from the extracted distribution with `python3 install.py --agent codex`,
`--agent claude-code`, `--agent opencode` or `--agent deepseek-harness`.
Codex defaults to `~/.agents/skills`; Harness defaults to `~/.dsh/skills` and
respects `DSH_HOME`. Run installation on the machine hosting the agent.
`--destination PATH` selects another
parent skill directory. The installer creates independent copies, each with one
entrypoint and its own resources: one main skill and eight specialized skills. Reinstall from a new distribution to update;
previous managed copies are retained in a hidden backup directory outside the
skill scan root. Entrypoints are regular files. Check the agent's skill catalog
after installation; file integrity alone does not prove discovery.

All entrypoints share the [direct writing policy](assertive-writing.md),
Times New Roman / SimSun defaults, inward ticks and separate explanatory captions.
See [writing modes](v3-migration.md) for the optional legacy route.

The source repository and download package store shared resources once at the
root. `subskills/` contains the eight entrypoints and their agent metadata;
use the root installer instead of copying a subskill directory by itself.
The installer resolves resource links into independent installed skills.
