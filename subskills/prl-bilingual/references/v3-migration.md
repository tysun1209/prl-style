# Writing modes

The default `assertive_calibrated` mode states supported results directly,
retains meaningful conditions and returns the requested text before optional
audit details. It applies to English, Chinese, captions and bilingual work.

```bash
python3 scripts/writing_profile.py
python3 scripts/writing_profile.py --mode legacy_v2
```

`legacy_v2` selects preserved earlier writing guides. Both modes retain the
current figure defaults and scientific-fidelity requirements. Claim ledgers
and optional audits use the templates under `assets/templates`.

`python3 scripts/verify_package.py` checks distributed-file integrity.
`python3 scripts/check_prl_environment.py` reports local font availability.
Compilation and final-page inspection apply to the user's actual manuscript;
package integrity does not establish manuscript typography or scientific quality.
The development environment did not complete exact-SimSun Chinese manuscript
validation; the font default remains SimSun.
