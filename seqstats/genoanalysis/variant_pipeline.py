# variant_pipeline.py
import subprocess
import os
from .utils import is_gzipped, check_executable

def run_pipeline(input_path, ref_path, output_vcf):
    if not os.path.exists(output_vcf):
        # 自动判断并构建 pipeline
        if input_path.endswith(".fastq.gz"):
            trimmed = input_path.replace(".fastq.gz", "_trimmed.fastq.gz")
            subprocess.run([
                "trimmomatic", "SE", "-threads", "2", input_path, trimmed,
                "SLIDINGWINDOW:4:20", "MINLEN:20"
            ])
            input_path = trimmed

        if input_path.endswith(".fastq.gz"):
            sam_out = output_vcf.replace(".vcf", ".sam")
            subprocess.run([
                "bwa", "mem", "-t", "2", ref_path, input_path, "-o", sam_out
            ])
            input_path = sam_out

        if input_path.endswith(".sam"):
            bam_out = input_path.replace(".sam", ".bam")
            subprocess.run([
                "samtools", "view", "-bt", ref_path, "-o", bam_out, input_path
            ])
            input_path = bam_out

        if input_path.endswith(".bam"):
            sorted_bam = input_path.replace(".bam", ".sorted.bam")
            subprocess.run(["samtools", "sort", "-o", sorted_bam, input_path])
            subprocess.run(["samtools", "index", sorted_bam])
            bcf = output_vcf.replace(".vcf", ".bcf")
            subprocess.run([
                "bcftools", "mpileup", "-O", "b", "-f", ref_path, sorted_bam, "-o", bcf
            ])
            subprocess.run([
                "bcftools", "call", "--ploidy", "1", "-m", "-v", "-o", output_vcf, bcf
            ])
            subprocess.run([
                "vcfutils.pl", "varFilter", output_vcf, ">", output_vcf + ".filtered.vcf"
            ], shell=True)
