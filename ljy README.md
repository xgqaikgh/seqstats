
# 🔧 核心模块说明

| 模块文件                               | 功能说明                        |
| ---------------------------------- | --------------------------- |
| `variant_data.py`                  | VCF 文件加载、查询、统计和可视化          |
| `variant_pipeline.py`              | 从 FASTQ/SAM/BAM 到 VCF 的自动流程 |
| `format_convert_and_align.py`  | 多格式输入统一转为 FASTA 并生成 VCF     |

### ✅ format_convert_and_align.py模块功能说明

该模块包含两个函数:

1. convert_to_fasta(input_path, output_fasta)
将下列格式统一转换为 FASTA：
.gb, .gbk（GenBank）
.fasta.gz
.fasta, .fa
.sam → 自动转 .bam 再转 fasta
.bam → 用 samtools fasta 提取序列

2. call_variants_from_fasta(fasta_path, ref_path, output_vcf)
用以下流程完成变异调用：

```python
FASTA → 比对 → BAM → sorted BAM → VCF
   bwa + samtools + bcftools
```

使用方法示例

``` python
from seqstats.genoanalysis.format_convert_and_align import convert_to_fasta, call_variants_from_fasta

# 输入文件（任意格式：.gb, .bam, .sam, .fasta.gz）

input_path = "example/CZB199.bam"
ref_path = "ref/ecoli_rel606.fasta"
intermediate_fasta = "tmp/CZB199.fasta"output_vcf = "vcfs/CZB199_converted.vcf"
# 转换为标准 FASTA
convert_to_fasta(input_path, intermediate_fasta)
# 与参考基因组比对并生成 VCF
call_variants_from_fasta(intermediate_fasta, ref_path, output_vcf)
```

### ✅`variant_data.py`

类名为 `VariantData`，提供查询、合并、绘图与导出功能。已确认其输入输出与项目兼容，无需修改。可通过以下方式调用：

```python
from genoanalysis.variant_data import VariantData
vd = VariantData(vcf_dir="vcfs", ref_fasta="ref/ecoli_rel606.fasta")
```

### ✅ `variant_pipeline.py`

用于从 `.fastq`, `.sam`, `.bam`, `.gb`, `.gbk`, `.genbank` 等输入生成 `.vcf` 文件。内部将调用：

- `bwa`, `samtools`, `bcftools` 命令行
- `Bio.SeqIO` 解析 GenBank/FASTA
- 输出兼容 `variant_data.py`
