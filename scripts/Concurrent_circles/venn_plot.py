"""
Concurrent circles (Venn-like) visualization of analytics per data type.

This module builds a high-resolution figure with four overlapping circles for
the following data types: Numeric, Sequence, Categorical, and Date. Labels for
analytics are placed in appropriate overlap regions. The function is designed
for legibility in papers: large default canvas, large fonts, and optional
static export (PNG/SVG) using Plotly + Kaleido.

Usage example:

    from scripts.Concurrent_circles.venn_plot import create_concurrent_circles_figure

    fig = create_concurrent_circles_figure(
        width=2000,
        height=1500,
        font_size=26,
    )
    fig.write_html("concurrent_circles.html")
    # Optional static export (requires kaleido)
    fig.write_image("concurrent_circles.png", scale=2)  # Very high resolution

"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Tuple, Set, FrozenSet

import plotly.graph_objects as go


def _add_circle(
    fig: go.Figure,
    center: Tuple[float, float],
    radius: float,
    fillcolor: str,
    opacity: float,
    line_color: str,
) -> None:
    """Add a circle shape to a Plotly figure.

    The circle is defined in data coordinates using the equation-based ellipse
    parameters (x0, y0, x1, y1) where x0/y0 and x1/y1 represent the bounding
    box corners.
    """

    cx, cy = center
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=cx - radius,
        y0=cy - radius,
        x1=cx + radius,
        y1=cy + radius,
        line=dict(color=line_color, width=3),
        fillcolor=fillcolor,
        opacity=opacity,
        layer="below",
    )


def _add_text_points(
    fig: go.Figure,
    labels: Iterable[Tuple[str, float, float]],
    font_size: int,
) -> None:
    """Add text-only scatter points.

    Each label tuple is (text, x, y).
    """

    if not labels:
        return

    fig.add_trace(
        go.Scatter(
            x=[x for _, x, _ in labels],
            y=[y for _, _, y in labels],
            text=[t for t, _, _ in labels],
            mode="text",
            textposition="middle center",
            textfont=dict(size=font_size, color="#1f1f1f"),
            hoverinfo="text",
            showlegend=False,
        )
    )


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  # type: ignore


def _rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return '#%02x%02x%02x' % rgb


def _blend_colors(hex_colors: List[str]) -> str:
    if not hex_colors:
        return '#1f1f1f'
    rs, gs, bs = 0, 0, 0
    for h in hex_colors:
        r, g, b = _hex_to_rgb(h)
        rs += r
        gs += g
        bs += b
    n = len(hex_colors)
    return _rgb_to_hex((int(rs / n), int(gs / n), int(bs / n)))


def _darken_hex(hex_color: str, factor: float) -> str:
    factor = max(0.0, min(1.0, float(factor)))
    r, g, b = _hex_to_rgb(hex_color)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return _rgb_to_hex((r, g, b))


def _avoid_label_overlap(
    labels: List[Tuple[str, float, float]],
    anchors: List[Tuple[float, float]],
    font_size: int,
    iterations: int = 220,
    step: float = 0.07,
    x_bounds: Tuple[float, float] = (0.4, 9.6),
    y_bounds: Tuple[float, float] = (0.4, 9.6),
    clusters: List[FrozenSet[str]] | None = None,
    cluster_penalty: float = 2.0,
    anchor_strength: float = 0.04,
) -> List[Tuple[str, float, float]]:
    """Iteratively repel labels to reduce overlaps while keeping them near anchors.

    Uses a simple force-based relaxation that treats each label as a disk with
    a radius roughly proportional to its text length and font size. This is a
    heuristic; it prioritizes legibility and stability over geometric precision.
    """

    texts = [t for t, _, _ in labels]
    xs = [x for _, x, _ in labels]
    ys = [y for _, _, y in labels]

    scale = max(0.5, min(2.0, font_size / 26.0))
    radii = [0.12 * scale + 0.006 * len(t) * scale for t in texts]

    for _ in range(max(0, iterations)):
        # pairwise repulsion
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                dx = xs[i] - xs[j]
                dy = ys[i] - ys[j]
                dist2 = dx * dx + dy * dy
                min_d = radii[i] + radii[j]
                # Inflate required spacing for labels from different clusters
                if clusters is not None and clusters[i] != clusters[j]:
                    min_d *= 1.0 + 0.08 * max(0.0, cluster_penalty)
                if dist2 == 0.0:
                    dx, dy = 0.001, 0.0
                    dist2 = dx * dx + dy * dy
                dist = dist2 ** 0.5
                if dist < min_d:
                    push = (min_d - dist) / max(min_d, 1e-6)
                    # Amplify repulsion for labels from different clusters
                    if clusters is not None and clusters[i] != clusters[j]:
                        push *= max(1.0, cluster_penalty)
                    ux = dx / dist
                    uy = dy / dist
                    xs[i] += ux * step * push
                    ys[i] += uy * step * push
                    xs[j] -= ux * step * push
                    ys[j] -= uy * step * push

        # gentle pull back to anchors and clamp to bounds
        for i in range(len(xs)):
            ax, ay = anchors[i]
            xs[i] += (ax - xs[i]) * anchor_strength
            ys[i] += (ay - ys[i]) * anchor_strength
            xs[i] = max(x_bounds[0], min(x_bounds[1], xs[i]))
            ys[i] = max(y_bounds[0], min(y_bounds[1], ys[i]))

    return [(texts[i], xs[i], ys[i]) for i in range(len(xs))]


def create_concurrent_circles_figure(
    width: int = 2000,
    height: int = 1500,
    font_size: int = 26,
    circle_opacity: float = 0.55,
    shared_region: float = 0.0,
    label_separation: float = 0.9,
    cluster_penalty: float = 2.0,
    cluster_spread: float = 0.7,
    grid_step: float = 0.04,
    region_padding: float = 0.03,
    region_spacing: float = 0.20,
    spacing_1way: float = -1.0,
    spacing_2way: float = -1.0,
    spacing_3way: float = -1.0,
    spacing_4way: float = -1.0,
    color_strength: float = 0.55,
) -> go.Figure:
    """Create the concurrent circles figure.

    Parameters
    ----------
    width : int
        Figure width in pixels. Defaults to 2000 for print-friendly export.
    height : int
        Figure height in pixels. Defaults to 1500 for print-friendly export.
    font_size : int
        Font size used for analytics labels.
    circle_opacity : float
        Fill opacity for the circles in [0, 1].

    Returns
    -------
    plotly.graph_objects.Figure
        The configured Plotly figure. Use write_html or write_image to export.
    """

    # Canvas coordinate system. We use a square-ish plane that comfortably fits
    # four overlapping circles and all labels without clipping.
    x_range = (0.0, 10.0)
    y_range = (0.0, 10.0)

    # Circle layout (centers and a common radius) tuned to resemble the sample
    # image while leaving room for clear labels.
    radius = 4.15
    base_centers = {
        "Numeric": (3.3, 6.3),
        "Sequence": (7.0, 6.2),
        "Categorical": (6.0, 3.2),
        "Date": (3.1, 3.3),
    }

    # Strong, fixed tones for higher contrast
    colors = {
        "Numeric": "#1E5BFF",      # strong blue
        "Sequence": "#2E7D32",     # strong green
        "Categorical": "#C62828",  # strong red
        "Date": "#5A2ECC",         # strong purple
    }

    # Interpolate centers toward their centroid based on shared_region in [0, 1]
    shared_region = max(0.0, min(1.0, shared_region))
    centroid_x = sum(c[0] for c in base_centers.values()) / 4.0
    centroid_y = sum(c[1] for c in base_centers.values()) / 4.0
    centers = {}
    for name, (cx, cy) in base_centers.items():
        nx = centroid_x + (cx - centroid_x) * (1.0 - shared_region)
        ny = centroid_y + (cy - centroid_y) * (1.0 - shared_region)
        centers[name] = (nx, ny)

    fig = go.Figure()

    # Draw the four circles
    for name in ["Numeric", "Sequence", "Categorical", "Date"]:
        _add_circle(
            fig,
            center=centers[name],
            radius=radius,
            fillcolor=colors[name],
            opacity=circle_opacity,
            line_color=colors[name],
        )

    # Labels with hand-tuned coordinates to reflect the overlaps as shown
    # in the reference image. Coordinates are in the same units as the axes.
    # Define base labels with their owning region membership. The membership is
    # used to keep labels in the correct overlap even when shared_region is large.
    LabelInfo = Tuple[str, Tuple[float, float], Set[str]]
    base_labels: List[LabelInfo] = [
        # Global / multi-type metrics (central region)
        ("Description", (5.0, 5.2), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Missing Percentage", (5.7, 4.7), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Samples", (4.6, 5.4), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Most Frequent Values", (5.0, 3.9), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Cardinality", (6.1, 4.2), {"Numeric", "Sequence", "Categorical", "Date"}),
        ("Uniqueness Ratio", (5.0, 3.3), {"Numeric", "Sequence", "Categorical", "Date"}),

        # Numeric-only (left/top zones)
        ("Quantiles", (3.8, 8.1), {"Numeric"}),
        ("Average Value", (2.6, 6.7), {"Numeric"}),

        # Sequence-only
        ("Maximum Length", (8.1, 7.2), {"Sequence"}),
        ("Mean Length", (8.5, 5.3), {"Sequence"}),
        ("Minimum Length", (6.7, 8.7), {"Sequence"}),

        # Numeric ∩ Sequence
        ("Frequency", (5.5, 6.8), {"Numeric", "Sequence"}),
        ("Uniformity", (5.8, 7.6), {"Numeric", "Sequence"}),

        # Sequence ∩ Categorical
        ("Unique Count", (6.5, 6.8), {"Numeric", "Sequence"}),

        # Numeric ∩ Date (left/bottom region)
        ("Minimum Value", (2.0, 4.6), {"Numeric", "Date"}),
        ("Maximum Value", (2.6, 2.9), {"Numeric", "Date"}),

        # Categorical ∩ Date (bottom center)
        ("Distribution", (5.0, 1.9), {"Categorical", "Date"}),
    ]

    # Compute label positions that stay in their intended regions.
    labels: List[Tuple[str, float, float]] = []
    label_anchors: List[Tuple[float, float]] = []
    label_clusters: List[FrozenSet[str]] = []
    all_types = {"Numeric", "Sequence", "Categorical", "Date"}
    # Region-size dependent minimum radial factors to prevent collapsing
    # into the center when shared_region is large.
    min_factor_by_size = {1: 0.90, 2: 0.70, 3: 0.55, 4: 0.35}

    for text, (lx, ly), region in base_labels:
        region_size = len(region)
        min_factor = min_factor_by_size.get(region_size, 0.6)
        factor = max(min_factor, 1.0 - shared_region)

        # Compute position by pulling the original base label toward centroid
        # with a factor that depends on membership size.
        nx = centroid_x + (lx - centroid_x) * factor
        ny = centroid_y + (ly - centroid_y) * factor

        # Store as both initial position and anchor; a later relaxation step
        # will resolve any residual overlaps while keeping labels near anchors.
        labels.append((text, nx, ny))
        label_anchors.append((nx, ny))
        label_clusters.append(frozenset(region))

    # Replace heuristic spreading with mathematically defined region placement.
    # 1) Build candidate grid
    step = max(0.01, float(grid_step))  # grid step in axis units
    xs_grid = [x_range[0] + step * i for i in range(int((x_range[1] - x_range[0]) / step) + 1)]
    ys_grid = [y_range[0] + step * j for j in range(int((y_range[1] - y_range[0]) / step) + 1)]

    def in_circle(px: float, py: float, cxy: Tuple[float, float]) -> float:
        dx = px - cxy[0]
        dy = py - cxy[1]
        return (dx * dx + dy * dy) ** 0.5

    # 2) Precompute candidate points per region key
    region_to_points: Dict[FrozenSet[str], List[Tuple[float, float, float]]] = {}
    all_types_set = {"Numeric", "Sequence", "Categorical", "Date"}
    for ky in set(label_clusters):
        included = list(ky)
        excluded = list(all_types_set - set(ky))
        candidates: List[Tuple[float, float, float]] = []
        for px in xs_grid:
            for py in ys_grid:
                # inside all included
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
                # outside all excluded
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
        # sort by margin (prefer interior points)
        candidates.sort(key=lambda p: p[2], reverse=True)
        region_to_points[ky] = candidates

    # 3) Greedy placement per region using candidate points
    placed: List[Tuple[float, float, float, FrozenSet[str]]] = []  # (x,y,r,key)
    new_labels: List[Tuple[str, float, float]] = [(t, 0.0, 0.0) for t, _, _ in labels]

    def label_radius(text: str) -> float:
        scale = max(0.5, min(2.0, font_size / 26.0))
        return 0.12 * scale + 0.007 * len(text) * scale

    # indices grouped by region size high -> low to fill central first
    indices_by_key: Dict[FrozenSet[str], List[int]] = {}
    for idx, key in enumerate(label_clusters):
        indices_by_key.setdefault(key, []).append(idx)
    ordered_keys = sorted(indices_by_key.keys(), key=lambda k: (-len(k), tuple(sorted(k))))

    for key in ordered_keys:
        idxs = indices_by_key[key]
        candidates = region_to_points.get(key, [])
        if not candidates:
            # Fallback to previous anchor if region has no area (rare)
            for i in idxs:
                text, ax, ay = labels[i]
                new_labels[i] = (text, ax, ay)
                placed.append((ax, ay, label_radius(text)))
            continue
        # try to place labels greedily
        for i in idxs:
            text = labels[i][0]
            r_need = label_radius(text)
            chosen = None
            best_score = -1e9
            # Region-specific spacing. If explicit per-size spacing not provided
            # (negative), fall back to global region_spacing scaled as before.
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
                # compute distance to existing placed labels
                ok = True
                min_dist = float("inf")
                for (qx, qy, qr, qkey) in placed:
                    d = ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5
                    req = qr + r_need
                    if qkey == key:
                        req += same_region_extra
                    min_dist = min(min_dist, d - req)
                    if d < req:
                        ok = False
                        break
                if not ok:
                    continue
                # ensure the label disk fits fully in region by margin
                if margin < (r_need + float(region_padding)):
                    continue
                score = margin + 0.5 * min_dist
                if score > best_score:
                    best_score = score
                    chosen = (px, py)
            if chosen is None:
                # relax constraint: take top-margin candidate even if overlaps slightly
                px, py, _ = candidates[0]
                new_labels[i] = (text, px, py)
                placed.append((px, py, r_need, key))
            else:
                px, py = chosen
                new_labels[i] = (text, px, py)
                placed.append((px, py, r_need, key))

    labels = new_labels

    # Styled annotations: bold text, white rounded box, stroke colored by region
    color_by_type = {
        "Numeric": colors["Numeric"],
        "Sequence": colors["Sequence"],
        "Categorical": colors["Categorical"],
        "Date": colors["Date"],
    }
    for (text, x, y), key in zip(labels, label_clusters):
        region_colors = [_hex_to_rgb(color_by_type[t]) for t in key]
        hex_colors = [color_by_type[t] for t in key]
        border_color = _blend_colors(hex_colors)
        fig.add_annotation(
            x=x,
            y=y,
            text=f"<b>{text}</b>",
            showarrow=False,
            xref="x",
            yref="y",
            font=dict(size=font_size, color=border_color),
            align="center",
            bgcolor="#ffffff",
            bordercolor=border_color,
            borderwidth=2,
            borderpad=4,
        )

    # Axis and layout styling for publication-quality output
    fig.update_xaxes(
        visible=False,
        range=x_range,
        constrain="range",
        scaleanchor="y",
        scaleratio=1,
    )
    fig.update_yaxes(visible=False, range=y_range, constrain="range")

    # Corner badges for the circle names
    badge_font = max(int(font_size * 0.9), 18)
    fig.update_layout(
        width=width,
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        annotations=[
            # Top badges swapped to match left/right semantics
            dict(
                text="<b>Numeric</b>",
                x=0.08,
                y=0.95,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color="#ffffff", size=badge_font),
                bgcolor=colors["Numeric"],
                bordercolor=colors["Numeric"],
                borderpad=6,
                align="center",
            ),
            dict(
                text="<b>Sequence</b>",
                x=0.92,
                y=0.95,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color="#ffffff", size=badge_font),
                bgcolor=colors["Sequence"],
                bordercolor=colors["Sequence"],
                borderpad=6,
                align="center",
            ),
            dict(
                text="<b>Categorical</b>",
                x=0.92,
                y=0.06,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color="#ffffff", size=badge_font),
                bgcolor=colors["Categorical"],
                bordercolor=colors["Categorical"],
                borderpad=6,
                align="center",
            ),
            dict(
                text="<b>Date</b>",
                x=0.08,
                y=0.06,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color="#ffffff", size=badge_font),
                bgcolor=colors["Date"],
                bordercolor=colors["Date"],
                borderpad=6,
                align="center",
            ),
        ],
    )

    return fig


__all__ = ["create_concurrent_circles_figure"]


