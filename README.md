# lmdixon23.github.io

Public research site for Logan Dixon, live at <https://lmdixon23.github.io/>.

The site presents current mathematical research, reproducible repositories, AI systems work, and interactive teaching tools. It is a static site with no application framework, advertising, or behavioral tracking.

## Verify locally

Use Python 3.13 or a recent Python 3 release:

```bash
bash run_all.sh
```

The expected final line is:

```text
VERDICT: SITE VERIFIED
```

The verification suite checks the SHA-256 manifest, required metadata, structured data, local assets, internal anchors, accessibility-critical HTML attributes, prohibited local paths, and the deployment file set. Text-file hashes use canonical LF line endings; binary assets are checked byte for byte.

## Preview locally

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/>.

## Repository map

- `index.html`: canonical site
- `404.html`: custom not-found page
- `preview.png`: current social preview artwork
- `scripts/`: deterministic repository checks
- `.github/workflows/deploy-pages.yml`: verify, package, and deploy workflow
- `SHA256SUMS.txt`: integrity boundary for canonical public files

GitHub Actions deploys a minimal `_site` artifact containing only files needed by the public website.
