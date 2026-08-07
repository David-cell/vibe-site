# Vibe Coding Tools

Free, privacy-first, 100% client-side developer tools (prompt builder, AI cost
calculator, LLM model compare, CLAUDE.md generator, project brief generator, AI
PR review + security checklists) plus hands-on blog comparisons.

## Project layout

```
vibe-site/
├── build_site.py        # static site generator (Python 3)
├── data/models.json     # ← MODEL PRICING / COMPARISON DATA (edit this to update prices)
├── site.css             # shared styles
├── netlify.toml         # build config for Git auto-deploy
├── index.html           # generated (do not edit by hand)
├── <tool>.html          # generated tool pages
├── blog/                # generated blog pages
└── ...
```

## Updating model prices (real-time data)

All model pricing and the comparison table live in **`data/models.json`** — the
single source of truth. To change a price or add a model:

1. Edit `data/models.json` (fields: `id`, `label`, `context`, `in`, `out`,
   `use`, `best`).
2. Commit and push to the connected Git repo.
3. Netlify rebuilds `build_site.py` automatically and the new prices go live —
   no manual Python run, no re-uploading a zip.

You never need to touch `build_site.py` or the generated HTML to update data.

## Building locally

```bash
python build_site.py
```

This regenerates every HTML page from the source data. Open `index.html` via a
local server (`python -m http.server`) to preview.

## Deploying (Git auto-deploy)

1. Push this folder to a GitHub/GitLab repo.
2. In Netlify: **Add new site → Import an existing project** → connect the repo.
3. Netlify reads `netlify.toml`:
   - Build command: `python build_site.py`
   - Publish directory: `.`
4. Set the custom domain `vibe.david-cells.com` (DNS already covers subdomains
   via the `TXT @` record) and add a GSC property for it.

Every future `git push` to the production branch triggers a fresh build + deploy.

## Notes

- Affiliate links in `build_site.py` (`AFF_BY_POST`) are placeholders
  (`https://example.com/aff/*`) — replace with real Impact/partner URLs before
  earning.
- `ads.txt` carries the real AdSense publisher ID; `CONTACT_EMAIL` is
  `hello@david-cells.com`.
