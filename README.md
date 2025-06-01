# README
## 功能
对 .sam、.bam、.fastq.gz 文件进行基本统计分析，并生成可视化图表。
分析目标：
读取并统计每个文件中的：
1. 总读取数
2. 比对成功的读取数（SAM/BAM）
3. 平均测序长度
4. 比对质量分布
5. 可视化：
6. 测序长度分布
7. 比对质量分布（仅 SAM/BAM）
## 结构
seqstats_pkg/
├── seqstats/                    # 主包
│   ├── __init__.py
│   ├── fastq_analysis.py        # FASTQ 分析
│   ├── sam_bam_analysis.py      # SAM/BAM 分析
│   ├── plot.py                  # 可视化
│   └── utils.py                 # 工具函数（如路径判断等）
├── example/                     # 示例目录
│   ├── SRR098026.fastq.gz
│   ├── SRR098026.sam
│   ├── SRR098026.bam
│   └── run_analysis.py          # 使用示例
├── setup.py                     # pip 安装脚本
├── README.md                    # 项目说明
└── requirements.txt             # 依赖列表
