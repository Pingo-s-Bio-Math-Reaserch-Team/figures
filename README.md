# BIBM Figure Reproducibility Package

This package contains the source tables, scripts, and documentation needed to recreate the manuscript figures and diagrams for the sheaf-theoretic glioma project.

## What this package does

- Regenerates manuscript figures from CSV source tables.
- Verifies key numeric claims against the bundled result tables.
- Provides a Google Colab notebook and local Python scripts.
- Saves regenerated figures as both `.pdf` and `.png`.
- Documents the provenance of every figure.

## What this package does not claim

This package recreates the figures from the finalized analysis tables. It does not redownload raw TCGA/CGGA omics matrices or rerun the entire raw-data-to-results pipeline. Raw-data execution is handled by the separate `multiomics_sheaf_production_pipeline_package.zip`.

## Quick local run

```bash
cd bibm_figure_reproducibility
pip install -r requirements.txt
python scripts/verify_results_from_tables.py
python scripts/reproduce_all_figures.py
```

## Google Colab run

Open `notebooks/BIBM_Figure_Reproduction_Colab.ipynb`, mount Google Drive, set `PROJECT_DIR`, and run all cells.

## Main outputs

Generated figures will appear in:

```text
figures/
```

Each figure is saved as:

```text
figure_name.pdf
figure_name.png
```

## Key integrity file

`checksums_and_validation.json` is produced by the verification script and records key result checks. `data_manifest_sha256.csv` records SHA256 hashes for all bundled source tables.
