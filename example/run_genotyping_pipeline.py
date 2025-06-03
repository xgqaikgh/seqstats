# example/run_format_convert.py
from seqstats.genoanalysis import run_pipeline

from seqstats.genoanalysis.format_convert_and_align_modified import convert_to_fasta, call_variants_from_alignment
import os
os.makedirs("vcfs", exist_ok=True)
os.makedirs("tmp", exist_ok=True)  # 如果你将中间文件放 tmp
os.makedirs("fasta", exist_ok=True)


input_path = "example/data/SRR098026.bam"  # 替换成你已有的 bam/sam/gbk 文件
ref_path = "ref/ecoli_rel606.fasta"
fasta_out = "fasta/SRR098026_converted.fasta"
vcf_out = "vcfs/SRR098026_from_convert.vcf"

# example/run_genotyping_pipeline.py

import os
from seqstats.genoanalysis import run_pipeline

# 示例输入：你可以换成 .bam / .sam / .gbk / .fasta / .fa.gz 等
input_files = [
    "example/data/SRR098026.bam",
    # "example/data/SRR098026.sam",
    # "example/data/SRR098026.gbk",
    # "example/data/SRR098026.fasta",
]

ref_path = "ref/ecoli_rel606.fasta"

# 创建输出目录
os.makedirs("vcfs", exist_ok=True)

for input_path in input_files:
    # 自动从文件名生成输出 VCF 路径
    basename = os.path.basename(input_path).split('.')[0]
    output_vcf = f"vcfs/{basename}.called.vcf"

    print(f"🚀 正在处理: {input_path}")
    run_pipeline(input_path, ref_path, output_vcf)
    print(f"✅ 生成完成: {output_vcf}\n")
