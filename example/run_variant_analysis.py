"""
Variant-focused analysis entrypoint for GenoAnalysis module.
This script loads VCFs and visualizes allele distributions using VariantData.
"""

from seqstats.genoanalysis.variant_data import VariantData
import os
import pandas as pd
import matplotlib.pyplot as plt

vcf_dir = "vcfs"
ref_fasta = "ref/ecoli_rel606.fasta"


vd = VariantData(vcf_dir=vcf_dir, ref_fasta=ref_fasta)

print("变异总数：", len(vd.variants))
print("前几个变异：")
for i, ((chrom, pos), data) in enumerate(sorted(vd.variants.items())[:5]):
    print(f"{i+1}. {chrom}:{pos}, ref={data['ref']}, alt={data['alt']}")

#  1：加载变异并打印区域结果
# 查询某段染色体区域变异
region_variants = vd.get_variants_in_interval("NC_012967.1", 100000, 101000)

print("区域内变异数量:", len(region_variants))
for v in region_variants:
    print(f"位置 {v['pos']}，参考: {v['ref']}，变异: {v['alt']}")



# 2：导出 CSV 
vd.export_to_csv("variants_export.csv")
print("已导出为 variants_export.csv")
df = pd.read_csv("variants_export.csv")
df.head()



