# GDPR analysis

Data, notebooks, and figures behind "Does GDPR Research Translate into Practice? An Analysis of EU-Funded Projects and Compliance Tools."

This `analysis/` directory is the only part of the project tracked in this repo — the manuscript source, bibliography, and the final copies of figures used in the paper live outside it.

## Data

- `gdpr_projects.csv` — 31 EU-funded GDPR-related projects, assembled from CORDIS and individual project pages. Funding figures are EU contribution amounts. CORDIS doesn't cover REC/CERV/Justice-programme grants, so those projects' dates and funding were cross-checked against the EU Funding & Tenders Portal directly.
- `enforcement-by-year.csv`, `enforcement-by-violation.csv`, `enforcement-violation-by-year.csv` — export from the GDPR Enforcement Tracker (enforcementtracker.com, CMS Law), covering 2018–2026.

## Notebooks

- `01_thematic_clustering.ipynb` — TF-IDF and sentence-embedding (mpnet) clustering of the 31 projects, checked against funding levels.
- `02_funding_domain_heatmap.ipynb` — funding/domain/timeline figures, plus the Mann-Whitney, Shapiro-Wilk, and Fisher's exact tests reported in the paper. Source for most of the project-landscape figures.
- `03_gdpr_violations.ipynb` — violation-type and year-over-year figures from the enforcement tracker export.
- `tools_figures_verified.py` — regenerates the tool-comparison figures (article coverage, technology families) from the 19-tool dataset. Every row was checked against Crossref and the source paper before inclusion; see the script header for which entries were added or corrected and when.

## Regenerating figures

Each notebook reads its CSV from this directory and writes PNGs back into it:

```
jupyter nbconvert --to notebook --execute --inplace 02_funding_domain_heatmap.ipynb
```

Figures aren't copied into the manuscript's image folder automatically — that's a manual step after regenerating.

## Known gaps

A handful of fields (consortium size, country, total cost) are missing for projects outside CORDIS, since those programmes don't publish the same structured data CORDIS does.
