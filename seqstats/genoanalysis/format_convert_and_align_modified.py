
import os
import subprocess
from Bio import SeqIO
import gzip

def convert_to_fasta(input_path, output_fasta):
    """
    将输入的 GenBank (.gb/.gbk), gzipped FASTA, 或 SAM/BAM 文件统一转换为标准 FASTA 格式。
    """
    if input_path.endswith(".gb") or input_path.endswith(".gbk"):
        records = SeqIO.parse(input_path, "genbank")
        SeqIO.write(records, output_fasta, "fasta")

    elif input_path.endswith(".fasta.gz"):
        with gzip.open(input_path, "rt") as handle:
            records = SeqIO.parse(handle, "fasta")
            SeqIO.write(records, output_fasta, "fasta")

    elif input_path.endswith(".fasta") or input_path.endswith(".fa"):
        subprocess.run(["cp", input_path, output_fasta])

    elif input_path.endswith(".sam"):
        bam_path = input_path.replace(".sam", ".bam")
        subprocess.run(["samtools", "view", "-bS", input_path, "-o", bam_path])
        convert_to_fasta(bam_path, output_fasta)

    elif input_path.endswith(".bam"):
        subprocess.run(["samtools", "fasta", input_path, "-o", output_fasta])
    else:
        raise ValueError("Unsupported input format: " + input_path)

def call_variants_from_alignment(alignment_path, ref_path, output_vcf):
    """
    使用 BAM 或 SAM 文件与参考基因组比对并调用变异，生成 VCF 文件。
    """
    if alignment_path.endswith(".sam"):
        bam_path = alignment_path.replace(".sam", ".bam")
        subprocess.run(["samtools", "view", "-bt", ref_path, "-o", bam_path, alignment_path])
        alignment_path = bam_path

    if alignment_path.endswith(".bam"):
        sorted_bam = output_vcf.replace(".vcf", ".sorted.bam")
        subprocess.run(["samtools", "sort", "-o", sorted_bam, alignment_path])
        subprocess.run(["samtools", "index", sorted_bam])
        bcf = output_vcf.replace(".vcf", ".bcf")
        subprocess.run(["bcftools", "mpileup", "-O", "b", "-f", ref_path, sorted_bam, "-o", bcf])
        subprocess.run(["bcftools", "call", "--ploidy", "1", "-m", "-v", "-o", output_vcf, bcf])
    else:
        raise ValueError("Alignment file must be .bam or .sam")

def run_pipeline(input_path, ref_path, output_vcf):
    """
    自动识别输入格式并执行从转换到变异检测的完整流程。
    """
    if input_path.endswith((".fasta", ".fa", ".fasta.gz", ".gb", ".gbk")):
        fasta_path = output_vcf.replace(".vcf", ".converted.fasta")
        convert_to_fasta(input_path, fasta_path)
        sam_path = output_vcf.replace(".vcf", ".sam")
        subprocess.run(["bwa", "mem", "-t", "2", ref_path, fasta_path, "-o", sam_path])
        call_variants_from_alignment(sam_path, ref_path, output_vcf)
    elif input_path.endswith((".sam", ".bam")):
        call_variants_from_alignment(input_path, ref_path, output_vcf)
    else:
        raise ValueError("Unsupported input format: " + input_path)
