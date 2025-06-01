from seqstats import analyze_fastq, analyze_sam_bam, plot_read_lengths, plot_mapping_quality
import pandas as pd

# 输入路径
fastq_path = "SRR098026.fastq.gz"
sam_path = "SRR098026.sam"
bam_path = "SRR098026.bam"

# 分析
fastq_df = analyze_fastq(fastq_path)
sam_result = analyze_sam_bam(sam_path, "sam")
bam_result = analyze_sam_bam(bam_path, "rb")

# 合并长度数据并绘图
length_df = pd.concat([fastq_df, sam_result["df"][["read_length", "source"]], bam_result["df"][["read_length", "source"]]])
plot_read_lengths(length_df)

# 合并 mapping quality 并绘图
mq_df = pd.concat([sam_result["df"][["mapping_quality", "source"]], bam_result["df"][["mapping_quality", "source"]]])
plot_mapping_quality(mq_df)

# 打印统计信息
print("FASTQ total reads:", len(fastq_df))
print("SAM  total reads:", sam_result["total_reads"], "| mapped:", sam_result["mapped_reads"])
print("BAM  total reads:", bam_result["total_reads"], "| mapped:", bam_result["mapped_reads"])
