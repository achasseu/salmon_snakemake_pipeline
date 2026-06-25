#!/bin/bash

set -euo pipefail

module load bioinfo-tools
module load BEDTools/2.31.1
module load Salmon/1.10.1

usage() {
    echo "Usage: $0 -S SAMPLE_NAME -I SALMON_INDEX -O OUTPUT_DIR"
    exit 1
}

while getopts "S:I:O:" opt; do
    case $opt in
        S) SAMPLE_NAME="$OPTARG" ;;
        I) SALMON_INDEX="$OPTARG" ;;
        O) OUTPUT_DIR="$OPTARG" ;;
        *) usage ;;
    esac
done

if [[ -z "${SAMPLE_NAME:-}" || -z "${SALMON_INDEX:-}" || -z "${OUTPUT_DIR:-}" ]]; then
    usage
fi

PROJECT=$(echo "$SAMPLE_NAME" | cut -d "_" -f1)

R1=$(find "../$PROJECT/$SAMPLE_NAME" \
     -type f \
     -name "*_R1_*.fastq.gz" | sort | head -n1)

if [[ -z "$R1" ]]; then
    echo "ERROR: No R1 FASTQ found for $SAMPLE_NAME"
    exit 1
fi

R2="${R1/_R1_/_R2_}"

if [[ ! -f "$R2" ]]; then
    echo "ERROR: No R2 FASTQ found for $SAMPLE_NAME"
    exit 1
fi

OUTDIR="${OUTPUT_DIR}/${SAMPLE_NAME}"
mkdir -p "$OUTDIR"

echo "Running Salmon for $SAMPLE_NAME"

salmon quant \
    -i "$SALMON_INDEX" \
    -l A \
    -1 "$R1" \
    -2 "$R2" \
    -p 8 \
    -o "$OUTDIR"

echo "Finished $SAMPLE_NAME"