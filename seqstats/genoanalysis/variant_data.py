import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class VariantData:
    def __init__(self, vcf_dir, ref_fasta):
        self.vcf_dir = vcf_dir
        self.ref = self._load_ref(ref_fasta)
        self.samples = []
        self.variants = {}
        self._load_vcfs()

    def _load_ref(self, fasta_path):
        seqs = {}
        chrom = None
        seq = []
        with open(fasta_path) as f:
            for line in f:
                if line.startswith('>'):
                    if chrom:
                        seqs[chrom] = ''.join(seq)
                    chrom = line[1:].split()[0]
                    seq = []
                else:
                    seq.append(line.strip())
            if chrom:
                seqs[chrom] = ''.join(seq)
        return seqs

    def _load_vcfs(self):
        for fname in sorted(os.listdir(self.vcf_dir)):
            if not fname.endswith('.vcf'):
                continue
            sample = os.path.splitext(fname)[0]
            self.samples.append(sample)
            path = os.path.join(self.vcf_dir, fname)
            with open(path) as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    parts = line.strip().split('\t')
                    chrom, pos, ref, alt = parts[0], int(parts[1]), parts[3], parts[4].split(',')
                    fmt = parts[8].split(':')
                    sample_field = parts[9].split(':')[0]
                    allele = ref if sample_field.startswith('0') else alt[0]
                    key = (chrom, pos)
                    if key not in self.variants:
                        self.variants[key] = {'ref': ref, 'alt': alt, 'samples': {}}
                    self.variants[key]['samples'][sample] = allele

    def get_variants_in_interval(self, chrom, start, end, target_sample=None):
        result = []
        for (c, pos), data in self.variants.items():
            if c == chrom and start <= pos <= end:
                # 筛选特定样本
                samples_data = {}
                if target_sample:
                    if target_sample in data['samples']:
                        samples_data[target_sample] = data['samples'][target_sample]
                    else:
                        continue  # 跳过不包含目标样本的位点
                else:
                    samples_data = data['samples']
                
                result.append({
                    'chrom': c,
                    'pos': pos,
                    'ref': data['ref'],
                    'alt': data['alt'],
                    'samples': samples_data
                })
        return result

    def merge_variant(self, chrom, pos, target_samples=None):
        key = (chrom, pos)
        if key not in self.variants:
            return None
        data = self.variants[key]
        merged = {
            'chrom': chrom,
            'pos': pos,
            'ref': data['ref'],
            'alt': data['alt'],
            'samples': {}
        }
        # 筛选目标样本
        samples = target_samples if target_samples else self.samples
        for s in samples:
            merged['samples'][s] = data['samples'].get(s, data['ref'])
        return merged

    def variant_stats(self, chrom, pos, cit_status):
        merged = self.merge_variant(chrom, pos)
        if not merged:
            return None
        
        # 初始化统计字典
        stats = {
            'Cit+': {'ref': 0, 'alt': 0},
            'Cit-': {'ref': 0, 'alt': 0},
            'Unknown': {'ref': 0, 'alt': 0}
        }
        
        ref_allele = merged['ref']  # 参考等位基因
        
        # 遍历所有样本
        for sample, allele in merged['samples'].items():
            # 处理样本名称匹配（去除_final后缀）
            clean_sample = sample.replace('_final', '')
            
            # 获取样本状态
            status = cit_status.get(clean_sample, 'Unknown')
            
            # 分类ref/alt
            if allele == ref_allele:
                category = 'ref'
            else:
                category = 'alt'
            
            # 累加计数
            stats[status][category] += 1
        
        # 绘制双柱状图
        plt.figure(figsize=(10, 6))
        
        # 设置柱状图参数
        categories = ['Cit+', 'Cit-', 'Unknown']
        x_pos = np.arange(len(categories))  # 0, 1, 2
        bar_width = 0.35
        
        # 提取数据
        ref_counts = [stats[cat]['ref'] for cat in categories]
        alt_counts = [stats[cat]['alt'] for cat in categories]
        
        # 绘制柱状图
        plt.bar(x_pos - bar_width/2, ref_counts, width=bar_width, 
                label='Ref', color='#1f77b4', edgecolor='black')
        plt.bar(x_pos + bar_width/2, alt_counts, width=bar_width,
                label='Alt', color='#ff7f0e', edgecolor='black')
        
        # 图表装饰
        plt.xticks(x_pos, categories)
        plt.ylabel("Count", fontsize=12)
        plt.title(f"Variant {chrom}:{pos}\nAllele Distribution by Cit Status", 
                fontsize=14, pad=20)
        plt.legend(title='Allele Type')
        
        # 显示数值标签
        for i, (r, a) in enumerate(zip(ref_counts, alt_counts)):
            plt.text(i - bar_width/2, r + 0.1, str(r), ha='center')
            plt.text(i + bar_width/2, a + 0.1, str(a), ha='center')
        
        plt.tight_layout()
        plt.show()
        
        return stats

    def export_to_csv(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['Variant', 'Chrom', 'Position', 'Ref', 'Alt'] + self.samples
            writer.writerow(header)
            for idx, ((chrom, pos), data) in enumerate(sorted(self.variants.items(), key=lambda x: x[0])):
                row = [
                    f'Variant{idx+1}', chrom, pos, data['ref'], ','.join(data['alt'])
                ] + [data['samples'].get(s, data['ref']) for s in self.samples]
                writer.writerow(row)