# lmdixon23.github.io

Public research site for Logan Dixon, live at <https://lmdixon23.github.io/>.

The site presents current mathematical research, reproducible repositories, AI systems work, and interactive teaching tools. It is a static site with no application framework or advertising. It uses privacy-minimized aggregate analytics that honor DNT/GPC and a local opt-out; experiment values, student responses, names, email addresses, and arbitrary query strings are not sent.

## Current public highlights

- **AI Playgrounds** — current [v1.9.6 educational-software release](https://github.com/lmdixon23/ai-playgrounds/releases/tag/v1.9.6) with 15 multilingual, offline-ready learner labs, 15 Level-1 Quick Assigns, and a standalone HTML download for every lab. Learner interfaces and Quick Assigns support English, Simplified Chinese, Vietnamese, and Spanish; some supporting teaching materials have narrower language coverage. The release improves classroom draft recovery, keyboard navigation, and instructional accuracy. The broader manual file/lab audit remains unfinished. The immutable v1.0.1 historical snapshot remains archived at <https://doi.org/10.5281/zenodo.21854217>; that version DOI does not identify v1.9.6.
- **EvalCanary** — evaluator-migration diff tooling for fixed-corpus before/after verifier analysis, provenance, subgroup review, and CI policy gates.
- **Current mathematical research** — SONC nonseparability/exactness; asymptotic-polygon global inversion for planar ridge networks; the planar four-ridge Neural Jacobian counterexample and sharp hidden-width threshold; and colored braid groupoid representation kernels.

The historical `njc-separation` repository is retained for provenance but is not presented as a current manuscript.

## Verify locally

Use Python 3.13 or a recent Python 3 release:

```bash
bash run_all.sh
```

The expected final line is:

```text
VERDICT: SITE VERIFIED
```

The verification suite checks the SHA-256 manifest, required metadata, structured data, local assets, internal anchors, accessibility-critical HTML attributes, prohibited local paths, current public-research links, UTF-8 mojibake sentinels, and the deployment file set. Text-file hashes use canonical LF line endings; binary assets are checked byte for byte.

## Preview locally

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/>.

## Repository map

- `index.html`: canonical site
- `404.html`: custom not-found page
- `privacy.html`: aggregate-analytics privacy boundary and opt-out
- `projects/ai-playgrounds.html`: AI Playgrounds portfolio case study
- `preview.png`: current social preview artwork
- `scripts/`: deterministic repository checks
- `.github/workflows/deploy-pages.yml`: verify, package, and deploy workflow
- `SHA256SUMS.txt`: integrity boundary for canonical public files

GitHub Actions deploys a minimal `_site` artifact containing only files needed by the public website.
