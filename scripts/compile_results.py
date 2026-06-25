import os
import glob
import pandas as pd
import numpy as np

# List all salmon .sf files (results/ under current working dir)
results_dir = os.path.join(os.getcwd(), "results")
sf_files = sorted(glob.glob(os.path.join(results_dir, "**", "*.sf"), recursive=True))

if len(sf_files) == 0:
    raise SystemExit(f"No .sf files found in {results_dir!r}")

# Extract sample names robustly: parent dir name, fallback to filename stem
def sample_name_from_path(p):
    p = Path(p)
    return p.parent.name if p.parent.name else p.stem

sample_names = [sample_name_from_path(f) for f in sf_files]

# Create sample table
sample_table = pd.DataFrame({
    "file": sf_files,
    "sample": sample_names
})

# Function to import Salmon quantification for all samples
def import_salmon_counts(sf_files, sample_names):
    tx_counts = {}
    tx_lengths = {}
    for idx, sf in enumerate(sf_files):
        df = pd.read_csv(sf, sep='\t')
        df = df.set_index('Name')
        tx_counts[sample_names[idx]] = pd.to_numeric(df['NumReads'], errors='coerce').fillna(0.0)
        tx_lengths[sample_names[idx]] = pd.to_numeric(df['EffectiveLength'], errors='coerce')
    counts = pd.DataFrame(tx_counts)    # transcripts x samples (fills missing with NaN -> later fill)
    lengths = pd.DataFrame(tx_lengths)
    return counts.fillna(0.0), lengths

counts, efflen = import_salmon_counts(sf_files, sample_names)

# Compute TPM using canonical effective length (median across samples) in kb and guard zeros
def compute_tpm(counts, efflen):
    # efflen: transcripts x samples -> collapse to canonical per-transcript
    eff_canonical = efflen.median(axis=1, skipna=True).replace({0: np.nan})
    eff_kb = eff_canonical / 1000.0
    rpk = counts.div(eff_kb, axis=0).fillna(0.0)
    scaling = rpk.sum(axis=0).replace({0: np.nan})
    tpm = rpk.div(scaling, axis=1) * 1e6
    return tpm.fillna(0.0)

tpm = compute_tpm(counts, efflen)

# ensure results_dir exists, then write outputs
os.makedirs(results_dir, exist_ok=True)
sample_table.to_csv(os.path.join(results_dir, "sample_table.tsv"), sep='\t', index=False)
counts.to_csv(os.path.join(results_dir, "counts.tsv"), sep='\t', index=True)
tpm.to_csv(os.path.join(results_dir, "tpm.tsv"), sep='\t', index=True)
