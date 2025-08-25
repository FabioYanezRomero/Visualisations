from __future__ import annotations

from pathlib import Path
import math
from typing import List, Tuple, Set

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import FancyBboxPatch


def save_concurrent_circles_static(
    output_path: Path | str,
    width: int = 2000,
    height: int = 1500,
    font_size: int = 26,
    dpi: int = 200,
    shared_region: float = 0.0,
    cluster_penalty: float = 2.0,
    cluster_spread: float = 0.7,
    grid_step: float = 0.04,
    region_padding: float = 0.03,
    region_spacing: float = 0.20,
    spacing_1way: float = -1.0,
    spacing_2way: float = -1.0,
    spacing_3way: float = -1.0,
    spacing_4way: float = -1.0,
) -> None:
    """Save a static PNG/SVG using Matplotlib without external system deps.

    Parameters mirror the Plotly version for consistency. The drawing uses the
    same coordinate system and label positions as the interactive figure.
    """

    radius = 4.15
    base_centers = {
        "Numeric": (3.3, 6.3),
        "Sequence": (7.0, 6.2),
        "Categorical": (6.0, 3.2),
        "Date": (3.1, 3.3),
    }
    colors = {
        "Numeric": "#1E5BFF",      # strong blue
        "Sequence": "#2E7D32",     # strong green
        "Categorical": "#C62828",  # strong red
        "Date": "#5A2ECC",         # strong purple
    }

    LabelInfo = Tuple[str, Tuple[float, float], Set[str]]
    base_labels: List[LabelInfo] = [
        ("Description", (5.0, 5.2), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Missing Percentage", (5.7, 4.7), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Samples", (4.6, 5.4), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Most Frequent Values", (5.0, 3.9), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Cardinality", (6.1, 4.2), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Uniqueness Ratio", (5.0, 3.3), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Quantiles", (3.8, 8.1), {"Numeric"}),
        ("Average Value", (2.6, 6.7), {"Numeric"}),
        ("Maximum Length", (8.1, 7.2), {"Sequence"}),
        ("Mean Length", (8.5, 5.3), {"Sequence"}),
        ("Minimum Length", (6.7, 8.7), {"Sequence"}),
        ("Frequency", (5.5, 6.8), {"Numeric", "Sequence"}),
        ("Uniformity", (5.8, 7.6), {"Numeric", "Sequence"}),
        ("Unique Count", (6.5, 6.8), {"Numeric", "Sequence"}),
        ("Minimum Value", (2.0, 4.6), {"Numeric", "Date"}),
        ("Maximum Value", (2.6, 2.9), {"Numeric", "Date"}),
        ("Distribution", (5.0, 1.9), {"Categorical", "Date"}),
    ]

    # Interpolate centers and labels toward centroid based on shared_region
    shared_region = max(0.0, min(1.0, shared_region))
    centroid_x = sum(c[0] for c in base_centers.values()) / 4.0
    centroid_y = sum(c[1] for c in base_centers.values()) / 4.0
    centers = {}
    for name, (cx, cy) in base_centers.items():
        nx = centroid_x + (cx - centroid_x) * (1.0 - shared_region)
        ny = centroid_y + (cy - centroid_y) * (1.0 - shared_region)
        centers[name] = (nx, ny)
    labels: List[Tuple[str, float, float]] = []
    anchors: List[Tuple[float, float]] = []
    min_factor_by_size = {1: 0.90, 2: 0.70, 3: 0.55, 4: 0.35}
    for text, (lx, ly), region in base_labels:
        region_size = len(region)
        min_factor = min_factor_by_size.get(region_size, 0.6)
        factor = max(min_factor, 1.0 - shared_region)
        nx = centroid_x + (lx - centroid_x) * factor
        ny = centroid_y + (ly - centroid_y) * factor
        labels.append((text, nx, ny))
        anchors.append((nx, ny))

    # Region-defined placement via grid sampling identical to Plotly backend
    def in_circle(px: float, py: float, cxy: Tuple[float, float]) -> float:
        dx = px - cxy[0]
        dy = py - cxy[1]
        return (dx * dx + dy * dy) ** 0.5

    step = max(0.01, float(grid_step))
    xs_grid = [0.0 + step * i for i in range(int(10.0 / step) + 1)]
    ys_grid = [0.0 + step * j for j in range(int(10.0 / step) + 1)]
    all_types_set = {"Numeric", "Sequence", "Categorical", "Date"}
    region_to_points: dict = {}
    for ky in set(frozenset(r) for _, _, r in base_labels):
        included = list(ky)
        excluded = list(all_types_set - set(ky))
        candidates = []
        for px in xs_grid:
            for py in ys_grid:
                inside = True
                min_in_margin = float("inf")
                for t in included:
                    d = in_circle(px, py, centers[t])
                    if d > radius:
                        inside = False
                        break
                    min_in_margin = min(min_in_margin, radius - d)
                if not inside:
                    continue
                outside = True
                min_out_margin = float("inf")
                for t in excluded:
                    d = in_circle(px, py, centers[t])
                    if d < radius:
                        outside = False
                        break
                    min_out_margin = min(min_out_margin, d - radius)
                if not outside:
                    continue
                margin = min(min_in_margin, min_out_margin)
                candidates.append((px, py, margin))
        candidates.sort(key=lambda p: p[2], reverse=True)
        region_to_points[ky] = candidates

    placed: List[Tuple[float, float, float, Set[str]]] = []
    new_labels: List[Tuple[str, float, float]] = [(t, 0.0, 0.0) for t, _, _ in labels]

    def label_radius(text: str) -> float:
        scale = max(0.5, min(2.0, font_size / 26.0))
        return 0.12 * scale + 0.007 * len(text) * scale

    indices_by_key: dict = {}
    for idx, (_, _, region) in enumerate(base_labels):
        key = frozenset(region)
        indices_by_key.setdefault(key, []).append(idx)
    ordered_keys = sorted(indices_by_key.keys(), key=lambda k: (-len(k), tuple(sorted(k))))
    for key in ordered_keys:
        idxs = indices_by_key[key]
        candidates = region_to_points.get(key, [])
        if not candidates:
            for i in idxs:
                text, ax, ay = labels[i]
                new_labels[i] = (text, ax, ay)
                placed.append((ax, ay, label_radius(text), set(key)))
            continue
        for i in idxs:
            text = labels[i][0]
            r_need = label_radius(text)
            chosen = None
            best_score = -1e9
            fallback = {
                1: 0.40 * max(0.0, region_spacing),
                2: 0.60 * max(0.0, region_spacing),
                3: 0.75 * max(0.0, region_spacing),
                4: 1.00 * max(0.0, region_spacing),
            }
            spacing_by_size = {
                1: spacing_1way if spacing_1way >= 0.0 else fallback[1],
                2: spacing_2way if spacing_2way >= 0.0 else fallback[2],
                3: spacing_3way if spacing_3way >= 0.0 else fallback[3],
                4: spacing_4way if spacing_4way >= 0.0 else fallback[4],
            }
            same_region_extra = spacing_by_size.get(len(key), fallback[2])
            for (px, py, margin) in candidates:
                ok = True
                min_dist = float("inf")
                for (qx, qy, qr, qkey) in placed:
                    d = ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5
                    req = qr + r_need
                    if qkey == set(key):
                        req += same_region_extra
                    min_dist = min(min_dist, d - req)
                    if d < req:
                        ok = False
                        break
                if not ok:
                    continue
                if margin < (r_need + float(region_padding)):
                    continue
                score = margin + 0.5 * min_dist
                if score > best_score:
                    best_score = score
                    chosen = (px, py)
            if chosen is None:
                px, py, _ = candidates[0]
                new_labels[i] = (text, px, py)
                placed.append((px, py, r_need, set(key)))
            else:
                px, py = chosen
                new_labels[i] = (text, px, py)
                placed.append((px, py, r_need, set(key)))

    labels = new_labels

    # Convert pixel size to inches
    fig_w_in = width / dpi
    fig_h_in = height / dpi
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), dpi=dpi)
    ax.set_facecolor("#ffffff")

    # Draw circles
    for name in ["Numeric", "Sequence", "Categorical", "Date"]:
        cx, cy = centers[name]
        circle = Circle((cx, cy), radius=radius, facecolor=colors[name], alpha=0.35, edgecolor=colors[name], linewidth=2)
        ax.add_patch(circle)

    # Labels
    # Draw labels with bold text inside white rounded boxes colored by region
    color_by_type = {
        "Numeric": colors["Numeric"],
        "Sequence": colors["Sequence"],
        "Categorical": colors["Categorical"],
        "Date": colors["Date"],
    }
    for (text, x, y), (_, _, region) in zip(labels, base_labels):
        if len(region) == 1:
            border_hex = color_by_type[next(iter(region))]
        else:
            # average colors for multi-type regions
            import matplotlib.colors as mcolors
            rgbs = [mcolors.to_rgb(color_by_type[t]) for t in region]
            avg = tuple(sum(c[i] for c in rgbs) / len(rgbs) for i in range(3))
            border_hex = mcolors.to_hex(avg)
        box = dict(boxstyle="round,pad=0.35", facecolor="#ffffff", edgecolor=border_hex, linewidth=2)
        ax.text(x, y, text, ha="center", va="center", fontsize=font_size, color=border_hex, bbox=box, fontweight="bold")

    # Corner badges
    badge_fs = max(int(font_size * 0.9), 18)
    # Top badges: Numeric (left), Sequence (right) to match circle positions
    ax.text(0.2, 0.94, "Numeric", transform=ax.transAxes, fontsize=badge_fs, color="white",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc=colors["Numeric"], ec=colors["Numeric"]))
    ax.text(0.8, 0.94, "Sequence", transform=ax.transAxes, fontsize=badge_fs, color="white",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc=colors["Sequence"], ec=colors["Sequence"]))
    ax.text(0.8, 0.06, "Categorical", transform=ax.transAxes, fontsize=badge_fs, color="white",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc=colors["Categorical"], ec=colors["Categorical"]))
    ax.text(0.2, 0.06, "Date", transform=ax.transAxes, fontsize=badge_fs, color="white",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc=colors["Date"], ec=colors["Date"]))

    # View limits and aspect
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 10.0)
    ax.set_aspect("equal")
    ax.axis("off")

    output_path = Path(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


__all__ = ["save_concurrent_circles_static"]


