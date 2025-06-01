import pysam
import pandas as pd

def analyze_sam_bam(file_path, filetype="sam"):
    read_lengths = []
    mapping_qualities = []
    mapped_reads = 0
    total_reads = 0

    samfile = pysam.AlignmentFile(file_path, filetype)
    for read in samfile.fetch(until_eof=True):
        total_reads += 1
        if not read.is_unmapped:
            mapped_reads += 1
            read_lengths.append(read.query_length)
            mapping_qualities.append(read.mapping_quality)
    samfile.close()
    return {
        "df": pd.DataFrame({
            "read_length": read_lengths,
            "mapping_quality": mapping_qualities,
            "source": filetype.upper()
        }),
        "total_reads": total_reads,
        "mapped_reads": mapped_reads
    }
