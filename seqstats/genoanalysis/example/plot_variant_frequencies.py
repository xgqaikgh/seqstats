"""
Visualize allele frequencies across all variant positions.
This script does not require sample classification.
"""

import os
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from seqstats.genoanalysis.variant_data import VariantData

# 初始化 VariantData
vcf_dir = "vcfs"
ref_fasta = "ref/ecoli_rel606.fasta"
vd = VariantData(vcf_dir=vcf_dir, ref_fasta=ref_fasta)

# 收集每个位点的等位基因频数
position_allele_counts = defaultdict(Counter)

for (chrom, pos), var in vd.variants.items():
    for sample, allele in var["samples"].items():
        position_allele_counts[(chrom, pos)][allele] += 1

# 只画前 10 个变异位点（可以改大）
top_positions = list(position_allele_counts.items())[:10]

# 画图
fig, axes = plt.subplots(len(top_positions), 1, figsize=(8, 3 * len(top_positions)), constrained_layout=True)

if len(top_positions) == 1:
    axes = [axes]

for ax, ((chrom, pos), allele_counts) in zip(axes, top_positions):
    ax.bar(allele_counts.keys(), allele_counts.values(), color="skyblue")
    ax.set_title(f"{chrom}:{pos}")
    ax.set_ylabel("Sample Count")
    ax.set_xlabel("Allele")

# 保存图像
plt.suptitle("Allele Frequency Distribution (Top 10 Variants)", fontsize=14)
plt.savefig("variant_frequencies.png")
print("图像已保存为 variant_frequencies.png")
