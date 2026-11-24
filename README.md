# Benjamini–Hochberg adjustments for childhood trauma biological ageing and pain

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24498705.svg)](https://doi.org/10.5281/zenodo.24498705)

## Cite this code

Hales, T. G. (2026). *BH adjustments for childhood trauma, biological ageing and chronic pain* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24498705


This package reproduces the final BH adjustments used for supplementary Tables S4–S8 and the mediation table. It contains 837 summary-level p values in 84 explicitly defined families, covering CTQ–pain, CTQ severity–pain, CTQ–EAA, CTQ severity–EAA, EAA–pain and mediation analyses. It does not contain participant-level data.

Version 1.0.0 is publicly released under the MIT licence and archived on Zenodo: https://doi.org/10.5281/zenodo.24498705. Earlier exploratory adjustment schemes and the separately numbered Supplementary Analyses 1–6 are outside this package.

## Run the analysis

Use Python 3.10 or later. The distributed scripts require only the Python standard library; Excel, R and additional Python packages are not required.

From this directory, run:

```sh
python bh_adjust.py
python validate.py
python -m unittest -v
```

The first command writes `results/bh_results.csv`. The validation command independently compares calculated q values with retained values from the completed analysis workbooks. The unit tests check a known example, ties, boundaries, invalid p values, incomplete families and separate adjustment of models.

Custom files can be supplied explicitly:

```sh
python bh_adjust.py --input data/tests.csv --families data/families.csv --output results/bh_results.csv
```

Run the full input together: deleting individual rows without redefining the families causes a family-size error.

## Multiplicity strategy

Model 1 is the primary analysis. Models 2 and 3 are follow-up analyses and receive the same within-family BH procedure separately. Tests are not combined across models, and no additional three-model multiplier is applied.

For sex-stratified cohort analyses, men and women and both cohorts (GS and MIDUS) contribute to the same family. Combined-sex results form separate families. Pooled analyses also form separate families from cohort-specific estimates; pooled estimates are not added to the GS/MIDUS family.

Each family listed below is defined separately for each model. “Sex-stratified” means women and men are included together in one family, not adjusted separately by sex.

| Analysis and test set | GS/MIDUS sex-stratified | GS/MIDUS combined sex | Pooled sex-stratified | Pooled combined sex |
| --- | ---: | ---: | ---: | ---: |
| CTQ–pain: total score | 4 | 2 | 2 | 1 |
| CTQ–pain: five subscales | 20 | 10 | 10 | 5 |
| CTQ–EAA: six clocks | 24 | 12 | 12 | 6 |
| EAA–pain: six clocks | 24 | 12 | 12 | 6 |
| Mediation: two primary GrimAge clocks | 8 | 4 | 4 | 2 |
| Mediation: four secondary clocks | 16 | 8 | 8 | 4 |

Severity analyses use the supplied pooled-cohort estimates. Low, Moderate and Severe are three contrasts relative to no childhood trauma:

| Severity analysis | Sex-stratified family | Combined-sex family |
| --- | ---: | ---: |
| CTQ severity–pain | 3 contrasts × 2 sexes = 6 | 3 |
| CTQ severity–EAA | 6 clocks × 3 contrasts × 2 sexes = 36 | 6 clocks × 3 contrasts = 18 |

Primary mediation families contain GrimAge1v2 and GrimAge2, reflecting the study's specified restriction following the EAA–pain analyses. Secondary families contain DunedinPACE, PhenoAge, Hannum and Horvath. This script reproduces those specified families; it does not repeat or statistically recalibrate the preceding selection step. Family-specific BH adjustments do not represent a single correction across all 837 tests.

## Algorithm and terminology

Within each family of size m, sort nominal p values as p(1) ≤ … ≤ p(m). Compute adjusted values by traversing ranks from m to 1:

```text
q(m) = min(1, p(m))
q(i) = min(q(i+1), m × p(i) / i)
```

Return the adjusted values in the original input order. In this manuscript these BH-adjusted p values are labelled “q values”; no separate estimation of the proportion of true null hypotheses is performed. The output flag uses q < 0.05. Values are calculated without display rounding.

The numerical p values are preserved at the precision supplied in the analysis spreadsheets. Their inclusion here does not imply greater precision than those source values. Strings such as `<0.001`, missing values, infinities and values outside [0,1] are rejected. Do not substitute a threshold or a rounded table p value when an underlying numeric value is available.

## Files and input columns

- `bh_adjust.py`: standalone calculation and command-line interface.
- `data/tests.csv`: one row per hypothesis, with test ID, family ID, analysis, scope, model, cohort, sex, measure and nominal p value.
- `data/families.csv`: one row per adjustment family, including its expected number of tests and readable definition. This file is the explicit family specification; the script does not infer families from filenames.
- `validation/expected_q.csv`: retained reference q values, family sizes and workbook/sheet/cell provenance.
- `validation/source_manifest.json`: reference workbook filenames and SHA-256 hashes.
- `validation/report.json`: validation result from preparation of this release candidate.
- `validate.py`: reproduction check with relative tolerance 1e-12 and absolute tolerance 1e-15.
- `test_bh.py`: unit tests.

All hypothesis IDs are unique. Each test belongs to exactly one family in this package. A family must contain the declared number of tests and a single matching model. The scripts do not estimate effects, fit regression or mediation models, pool cohorts, or edit manuscript tables.

The mediation table is headed “Table S8” in the current document but appears as S9 in its contents; it is identified by its analysis name here to avoid relying on that numbering discrepancy.

## Publication preparation

Version 1.0.0 was published on 24 November 2026 and archived on Zenodo at https://doi.org/10.5281/zenodo.24498705. The DOI identifies the archived release; subsequent changes to the main branch do not alter that archive.

Reference: Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society Series B. 1995;57:289–300.

## Corresponding Author

Full name: Tim G. Hales
Affiliation: School of Medicine, University of Dundee, Dundee, UK
ORCID: https://orcid.org/0000-0002-2040-9714
Contribution to the code or analysis: Statistical strategy and validation

The Python implementation and validation materials were prepared with assistance from OpenAI Codex and reviewed by Tim G. Hales.
