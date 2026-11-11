# PRL writing references

The writing cohort contains 100 PRL papers on particle motion, active particles
and reinforcement learning. The [public source index](writing-sources.json)
provides titles, DOIs, topics and the development/evaluation assignment.
The cohort has 80 development and 20 evaluation papers. The latter were already
inspected in an earlier revision and are not a pristine independent test set.

The current rules comprise 14 paired English/Chinese cards and two whole-article
guides under `corpus/writing-prl-100/v3/rules`. Use `scripts/writing_profile.py`
to resolve their locations. Cards retain source DOIs, pages/block locators,
paraphrased observations, counterexamples and applicable scope. Load only cards
relevant to the requested section and scientific task.

Chinese rules adapt the argument into natural Chinese. Font defaults and the
direct-delivery policy are project choices. Support counts describe selected
passages, not the prevalence of a writing pattern across the journal.

Original PDFs, extracted full text and development evaluation archives are not
included in the distribution. Follow the DOI when inspecting a source; source
hashes identify the versions used during development and are not proof that a
freshly downloaded file has been checked. The package integrity check verifies
the distributed rules, not the excluded papers. `legacy_v2` retains the older
editorial guides and rule cards for explicit compatibility requests.
