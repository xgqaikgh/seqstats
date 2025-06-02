# 📦 新包结构：`genoanalysis_pkg/`

genoanalysis_pkg/
├── genoanalysis/                         # 主功能包
│   ├── __init__.py
│   ├── fastq_analysis.py                 # FASTQ 分析
│   ├── sam_bam_analysis.py              # SAM/BAM 分析
│   ├── variant_data.py                   # VCF 查询/统计/可视化
│   ├── variant_pipeline.py               # 输入到 VCF 的一体化流程（含 GenBank 支持）
│   ├── plot.py                           # 通用可视化函数
│   └── utils.py                          # 公共函数：路径、格式判断等
├── example/
│   ├── SRR098026.fastq.gz
│   ├── SRR098026.sam
│   ├── SRR098026.bam
│   ├── test_example.ipynb               # 原始测试文件保留
│   ├── test_example.pdf
│   └── run_analysis.py                  # 统一的运行脚本
├── vcfs/                                 # 存放 vcf 文件
│   └── SRR098026_final.vcf
├── ref/                                  # 参考基因组/注释
│   ├── ecoli_rel606.fasta
│   └── ecoli_rel606.gtf
├── setup.py
├── requirements.txt
└── README.md

# 🔧 核心模块说明

### ✅`variant_data.py`

类名为 `VariantData`，提供查询、合并、绘图与导出功能。已确认其输入输出与项目兼容，无需修改。可通过以下方式调用：

```
from genoanalysis.variant_data import VariantData
vd = VariantData(vcf_dir="vcfs", ref_fasta="ref/ecoli_rel606.fasta")
```

### ✅ `variant_pipeline.py`

用于从 `.fastq`, `.sam`, `.bam`, `.gb`, `.gbk`, `.genbank` 等输入生成 `.vcf` 文件。内部将调用：

- `bwa`, `samtools`, `bcftools` 命令行
- `Bio.SeqIO` 解析 GenBank/FASTA
- 输出兼容 `variant_data.py`

### ✅ 统一入口：`run_analysis.py`

### 📦 打包配置（`setup.py`）

# ✅ 兼容性说明

- __未来扩展兼容__：可以保留 `genoanalysis/experimental/` 子模块放入 ChatGPT 另一段输出内容。
