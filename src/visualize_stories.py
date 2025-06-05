#!/usr/bin/env python3
"""
Visualization module for LLM story fixpoints.
This script uses sentence transformers to embed paragraphs from stories,
then creates a 2D PCA embedding plot where each line represents a story.
"""

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer
from story.manager import StoryManager

def load_stories(story_manager):
    """Load all stories from the cache directory."""
    retell_count = story_manager.load_cornerstones()[1]
    stories = []

    for i in range(retell_count + 1):
        story_text = story_manager.load_story(i)
        if story_text.strip():
            stories.append((i, story_text))  # Include iteration number as ID

    return stories

def split_into_paragraphs(text):
    """Split text into paragraphs."""
    # Use regex to split by double newlines, but keep the newlines in the paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def embed_paragraphs(model, stories):
    """Embed all paragraphs from all stories using a sentence transformer model."""
    all_data = []

    for story_id, story_text in stories:
        paragraphs = split_into_paragraphs(story_text)
        embeddings = model.encode(paragraphs)

        for paragraph_idx, (paragraph, embedding) in enumerate(zip(paragraphs, embeddings)):
            all_data.append({
                'story_id': story_id,
                'paragraph_idx': paragraph_idx,
                'paragraph_text': paragraph,
                'sentence_embedding': embedding
            })

    return pd.DataFrame(all_data)

def apply_pca(df):
    """Apply PCA to sentence embeddings and add 2D coordinates to the DataFrame."""
    # Extract all sentence embeddings
    all_embeddings = np.vstack(df['sentence_embedding'].to_numpy())

    # Apply PCA to reduce to 2 dimensions
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(all_embeddings)

    # Add the 2D coordinates back to the DataFrame
    df['pca1'] = reduced_embeddings[:, 0]
    df['pca2'] = reduced_embeddings[:, 1]

    return df

def apply_umap(df):
    """Apply UMAP to sentence embeddings and add 2D coordinates to the DataFrame."""
    # Extract all sentence embeddings
    all_embeddings = np.vstack(df['sentence_embedding'].to_numpy())

    # Apply UMAP to reduce to 2 dimensions
    umap_model = umap.UMAP(n_components=2, random_state=42)
    reduced_embeddings = umap_model.fit_transform(all_embeddings)

    # Add the 2D coordinates back to the DataFrame
    df['umap1'] = reduced_embeddings[:, 0]
    df['umap2'] = reduced_embeddings[:, 1]

    return df

def apply_tsne(df):
    """Apply t-SNE to sentence embeddings and add 2D coordinates to the DataFrame."""
    # Extract all sentence embeddings
    all_embeddings = np.vstack(df['sentence_embedding'].to_numpy())

    # Apply t-SNE to reduce to 2 dimensions
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings = tsne.fit_transform(all_embeddings)

    # Add the 2D coordinates back to the DataFrame
    df['tsne1'] = reduced_embeddings[:, 0]
    df['tsne2'] = reduced_embeddings[:, 1]

    return df

def plot_story_trajectories(df, method="pca", filename="story_embedding.png"):
    """Create a 2D embedding plot with lines for each story."""
    plt.figure(figsize=(15, 8))

    # Create a colormap
    cmap = plt.get_cmap('Spectral')
    num_stories = len(df['story_id'].unique())

    # Choose the right columns based on method
    x_col = f"{method}1"
    y_col = f"{method}2"

    # Group by story_id and plot each trajectory with a unique color
    groups = df.groupby('story_id')
    for idx, (name, group) in enumerate(groups):
        color = cmap(idx / num_stories)
        plt.plot(
            group[x_col],
            group[y_col],
            marker='.',
            markersize=0,
            linestyle='-',
            color=color,
            alpha=0.2
        )

    # replot the first and the last story with thicker lines
    for idx, (name, group) in enumerate(groups):
        color = cmap(idx / num_stories)
        if name == 0 or name == len(groups) - 1:
            plt.plot(
                group[x_col],
                group[y_col],
                marker='.',
                markersize=0,
                linestyle='-',
                color=color,
                alpha=1,
                zorder=10,
                linewidth=4,
                label=f'Story {name}'
            )

    title = f"2D {method.upper()} Embedding of Story Paragraphs"
    xlabel = f"{method.upper()} Component 1"
    ylabel = f"{method.upper()} Component 2"

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved {method.upper()} embedding plot to '{filename}'")

def main():
    """Main function to analyze and visualize stories."""
    # Initialize the sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load stories
    story_manager = StoryManager("seven sisters")
    stories = load_stories(story_manager)

    if not stories:
        print("No stories found.")
        return

    # Embed paragraphs from all stories and create DataFrame
    df = embed_paragraphs(model, stories)
    print(f"Created DataFrame with {len(df)} rows")

    # Apply all three methods and save separate files
    df_pca = apply_pca(df.copy())
    df_umap = apply_umap(df.copy())
    df_tsne = apply_tsne(df.copy())

    # Save the DataFrame to a file with all embeddings
    df.to_csv('story_embeddings.csv', index=False)
    print("Saved DataFrame to 'story_embeddings.csv'")

    # Plot and save each method separately
    plot_story_trajectories(df_pca, "pca", "story_embedding_pca.png")
    plot_story_trajectories(df_umap, "umap", "story_embedding_umap.png")
    plot_story_trajectories(df_tsne, "tsne", "story_embedding_tsne.png")

if __name__ == "__main__":
    main()