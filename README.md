# 🧬 Salmon Snakemake Pipeline

A reproducible and scalable RNA-seq quantification pipeline using **Salmon** and **Snakemake**, designed for HPC environments (SLURM).

This workflow performs transcript-level quantification from paired-end FASTQ files and generates per-sample abundance estimates.

---

## 📦 Overview

The pipeline:

1. Takes a list of RNA-seq samples
2. Automatically locates paired-end FASTQ files (R1/R2)
3. Runs **Salmon quantification**
4. Produces per-sample output directories containing `quant.sf`
5. Supports restartability and partial execution via Snakemake

---

## ⚙️ Requirements

### Software

- Snakemake
- Salmon ≥ 1.10
- Bash
- (Optional) SLURM cluster for parallel execution

### Modules (HPC example)

```bash
module load bioinfo-tools
module load Salmon/1.10.1