SAMPLES = [
    line.strip()
    for line in open("sample_list.txt")
    if line.strip()
]

SALMON_INDEX = "ERV_index_salmon"
OUTPUT_DIR = "erv_quant_lax"

rule all:
    input:
        expand(
            f"{OUTPUT_DIR}/{{sample}}/quant.sf",
            sample=SAMPLES
        )

rule salmon_quant:
    output:
        f"{OUTPUT_DIR}/{{sample}}/quant.sf"
    params:
        index=SALMON_INDEX,
        outdir=OUTPUT_DIR
    threads:
        8
    shell:
        """
        "../scripts/run_salmon.sh" \
            -S {wildcards.sample} \
            -I {params.index} \
            -O {params.outdir}
        """