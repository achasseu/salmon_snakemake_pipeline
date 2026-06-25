# Salmon Snakemake Pipeline

A small Snakemake pipeline and Bash wrappers to run Salmon quantification across sequencing samples. Intended to run on a local machine or an HPC cluster (SLURM).

## Requirements

- Snakemake (tested with Snakemake 6+)
- Salmon (quant) installed and available in PATH
- Bash
- (Optional) SLURM for cluster submission

## Repository layout

```
README.md
cluster/                 SLURM submission helper
  salmon_pipeline.sh
config/                  (optional config files; currently empty)
scripts/                 helper scripts
  run_salmon.sh
  compile_results.py
workflow/                Snakemake workflow
  Snakefile
  rules/                 (optional rule modules)
```

## Preparing your samples (sample_list)

The pipeline expects a `sample_list.txt` file listing one sample name per line. Each sample name should correspond to how your FASTQ files are named or arranged so the `scripts/run_salmon.sh` script can find the R1 and R2 files.

Supported FASTQ layout options (examples):

1) Paired files in a single directory with naming convention

- Example filenames for sample `SAMPLE1`:
  - SAMPLE1_R1.fastq.gz
  - SAMPLE1_R2.fastq.gz

2) Per-sample subdirectories where each sample has a directory named by the sample and contains the FASTQ files

- Directory structure:
  - reads/SAMPLE1/SAMPLE1_R1.fastq.gz
  - reads/SAMPLE1/SAMPLE1_R2.fastq.gz

How to create sample_list.txt

- Basic: one sample per line (no header)

```
SAMPLE1
SAMPLE2
SAMPLE3
```

- Save it at the repository root as `sample_list.txt`, or elsewhere and pass its path to Snakemake via the `--configfile` or by editing the Snakefile accordingly.

Note: The included Snakefile reads `sample_list.txt` from the working directory by default. If you want to put your sample list elsewhere or name it differently, either modify the Snakefile or call Snakemake from the directory where the file is located.

## How to run

- Dry-run the workflow (no execution):

```
snakemake -n
```

- Run locally using 8 threads (example):

```
snakemake -j 8
```

- Submit to SLURM using the provided wrapper (edit project/account and any other sbatch options):

```
./cluster/salmon_pipeline.sh
```

The `cluster/salmon_pipeline.sh` wrapper calls Snakemake with a cluster submission command like:

```
snakemake --jobs 50 --cluster "sbatch -A <PROJECT> -p core -t 10-00:00:00 -n 1" --rerun-incomplete --latency-wait 60
```

Replace `<PROJECT>` with your SLURM account/project. Consider editing the wrapper to make the project name an environment variable (e.g., SBATCH_PROJECT) or a script parameter.

- Run a single sample directly (script usage):

```
./scripts/run_salmon.sh -S SAMPLE_NAME -I /path/to/salmon_index -O /path/to/output_dir
```

The `run_salmon.sh` wrapper will try to locate R1/R2 files based on the sample name. If your naming scheme differs, either adapt the script or provide a per-sample directory layout that the script understands.

## Configuring the Snakefile

The Snakefile currently expects a plain `sample_list.txt` and has a small set of hard-coded names such as the OUTPUT_DIR and SAMPLE_INDEX symbols used inside the rule.


## Example minimal workflow run (end-to-end)

1. Create `sample_list.txt` in repo root:

```
Plate1_SAMPLE1
Plate2_SAMPLE2
```

2. Ensure your reads follow the naming layout the script expects (e.g., `SAMPLE1_R1.fastq.gz`, `SAMPLE1_R2.fastq.gz`) or adapt `scripts/run_salmon.sh`.

3. Run a dry-run to validate:

```
snakemake -n
```

4. Run the workflow:

```
snakemake -j 8
```

5. Run the results compiler:

```
python3 scripts/compile_results.py
```
