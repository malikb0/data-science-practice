"""Plotting theme and small figure helpers.

Matplotlib is imported lazily so that importing :mod:`ds_practice` (for data
loading or metrics) does not require the plotting stack.

``set_theme()`` gives every notebook the same look. The helpers return
``(fig, ax)`` so callers can keep customising the axes.
"""
from __future__ import annotations

from typing import Iterable


def _plt():
    import matplotlib.pyplot as plt

    return plt


def set_theme(context: str = "notebook", style: str = "whitegrid", palette: str = "deep") -> None:
    """Apply the shared Matplotlib/Seaborn theme."""
    try:
        import seaborn as sns

        sns.set_theme(context=context, style=style, palette=palette)
    except ImportError:
        plt = _plt()
        chosen = "seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "ggplot"
        plt.style.use(chosen)


def histogram(series: Iterable, bins: int = 20, title: str | None = None,
              xlabel: str | None = None, ax=None):
    """Histogram of a numeric series."""
    plt = _plt()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots()
    ax.hist(series, bins=bins, edgecolor="white")
    ax.set_title(title or "Distribution")
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig, ax


def barplot(x, y, title: str | None = None, xlabel: str | None = None,
            ylabel: str | None = None, ax=None):
    """Vertical bar chart."""
    plt = _plt()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots()
    ax.bar(x, y, edgecolor="white")
    ax.set_title(title or "")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig, ax


def scatterplot(x, y, title: str | None = None, xlabel: str | None = None,
                ylabel: str | None = None, ax=None):
    """Scatter plot."""
    plt = _plt()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots()
    ax.scatter(x, y, alpha=0.5, s=18)
    ax.set_title(title or "")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig, ax


def lineplot(x, y, title: str | None = None, xlabel: str | None = None,
             ylabel: str | None = None, ax=None):
    """Line plot."""
    plt = _plt()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots()
    ax.plot(x, y, marker="o")
    ax.set_title(title or "")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig, ax


def boxplot(data, title: str | None = None, ylabel: str | None = None, ax=None):
    """Box plot of one or more arrays."""
    plt = _plt()
    fig, ax = (ax.figure, ax) if ax is not None else plt.subplots()
    ax.boxplot(data)
    ax.set_title(title or "")
    if ylabel:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig, ax
