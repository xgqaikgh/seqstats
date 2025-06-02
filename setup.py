from setuptools import setup, find_packages

setup(
    name="seqstats",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pysam",
        "biopython",
        "matplotlib",
        "seaborn",
        "pandas",
        "notebook"
    ],
    author="Your Name",
    description="A toolkit for analyzing FASTQ, SAM, BAM files with visualizations.",
    python_requires='>=3.7',
)
