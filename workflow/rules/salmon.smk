rule salmon_quant:
    input:
        r1=lambda wc: config["samples_map"][wc.sample]["R1"],
        r2=lambda wc: config["samples_map"][wc.sample]["R2"]
    output:
        "results/{sample}/quant.sf"
    params:
        index=config["salmon_index"]
    threads: 8
    log:
        "logs/salmon/{sample}.log"
    shell:
        """
        mkdir -p results/{wildcards.sample} logs/salmon

        salmon quant \
            -i {params.index} \
            -l A \
            -1 {input.r1} \
            -2 {input.r2} \
            -p {threads} \
            -o results/{wildcards.sample} \
            > {log} 2>&1
        """