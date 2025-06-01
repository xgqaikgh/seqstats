import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_read_lengths(lengths_df, output="read_length_distribution.png"):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=lengths_df, x="read_length", hue="source", bins=50, kde=True)
    plt.title("Read Length Distribution")
    plt.xlabel("Read Length")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

def plot_mapping_quality(mapping_df, output="mapping_quality_distribution.png"):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=mapping_df, x="mapping_quality", hue="source", bins=50, kde=True)
    plt.title("Mapping Quality Distribution")
    plt.xlabel("Mapping Quality")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
