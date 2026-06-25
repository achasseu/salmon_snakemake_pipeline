#!/bin/bash

snakemake \
    --jobs 50 \
    --cluster "sbatch -A [PROJECT NAME] -p core -t 10-00:00:00 -n 1" \
    --rerun-incomplete \
    --latency-wait 60
