import gzip
from Bio import SeqIO
import pandas as pd

def analyze_fastq(fastq_file):
    read_lengths = []
    with gzip.open(fastq_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            read_lengths.append(len(record.seq))
    return pd.DataFrame({"read_length": read_lengths, "source": "FASTQ"})
