from __future__ import annotations

import argparse
from pathlib import Path

from .venn_plot import create_concurrent_circles_figure
from .venn_plot_mpl import save_concurrent_circles_static


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate concurrent circles (Venn-like) figure for analytics per data type.",
    )
    parser.add_argument("--width", type=int, default=2000, help="Figure width in pixels.")
    parser.add_argument("--height", type=int, default=1500, help="Figure height in pixels.")
    parser.add_argument("--font-size", type=int, default=26, help="Label font size.")
    parser.add_argument(
        "--shared-region",
        type=float,
        default=0.0,
        help="0.0=no change, 1.0=maximum concurrence (circles and labels pulled to centroid).",
    )
    parser.add_argument(
        "--cluster-penalty",
        type=float,
        default=2.0,
        help="Amplification factor for repulsion between labels from different clusters.",
    )
    parser.add_argument(
        "--cluster-spread",
        type=float,
        default=0.7,
        help="Radial spread of labels within the same cluster (higher = wider).",
    )
    parser.add_argument(
        "--grid-step",
        type=float,
        default=0.04,
        help="Grid sampling step for region placement (smaller = more precise, slower).",
    )
    parser.add_argument(
        "--region-padding",
        type=float,
        default=0.03,
        help="Extra clearance (in axis units) to keep label disk inside its region.",
    )
    parser.add_argument(
        "--region-spacing",
        type=float,
        default=0.20,
        help="Extra spacing between labels within the same region (axis units).",
    )
    parser.add_argument("--spacing-1way", type=float, default=-1.0, help="Override spacing for 1-way regions.")
    parser.add_argument("--spacing-2way", type=float, default=-1.0, help="Override spacing for 2-way regions.")
    parser.add_argument("--spacing-3way", type=float, default=-1.0, help="Override spacing for 3-way regions.")
    parser.add_argument("--spacing-4way", type=float, default=-1.0, help="Override spacing for 4-way regions.")
    parser.add_argument(
        "--html",
        type=Path,
        default=Path("concurrent_circles.html"),
        help="Path to save interactive HTML output.",
    )
    parser.add_argument(
        "--png",
        type=Path,
        default=None,
        help="Optional path to save PNG (Matplotlib backend, no system deps).",
    )
    parser.add_argument(
        "--svg",
        type=Path,
        default=None,
        help="Optional path to save SVG (Matplotlib backend).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2.0,
        help="Export scale factor for static images.",
    )
    parser.add_argument("--color-strength", type=float, default=0.55, help="Darkening factor for circle colors (0.2-1.0).")
    parser.add_argument("--circle-opacity", type=float, default=0.55, help="Fill opacity for circles (0-1).")
    args = parser.parse_args()

    fig = create_concurrent_circles_figure(
        width=args.width,
        height=args.height,
        font_size=args.font_size,
        shared_region=args.shared_region,
        cluster_penalty=args.cluster_penalty,
        cluster_spread=args.cluster_spread,
        grid_step=args.grid_step,
        region_padding=args.region_padding,
        region_spacing=args.region_spacing,
        spacing_1way=args.spacing_1way,
        spacing_2way=args.spacing_2way,
        spacing_3way=args.spacing_3way,
        spacing_4way=args.spacing_4way,
        color_strength=args.color_strength,
    )

    fig.write_html(str(args.html))
    # Static export via Matplotlib to avoid Chrome/Kaleido dependency
    if args.png is not None:
        save_concurrent_circles_static(
            output_path=args.png,
            width=args.width,
            height=args.height,
            font_size=args.font_size,
            dpi=int(96 * args.scale),
            shared_region=args.shared_region,
            cluster_penalty=args.cluster_penalty,
            cluster_spread=args.cluster_spread,
            grid_step=args.grid_step,
            region_padding=args.region_padding,
            region_spacing=args.region_spacing,
            spacing_1way=args.spacing_1way,
            spacing_2way=args.spacing_2way,
            spacing_3way=args.spacing_3way,
            spacing_4way=args.spacing_4way,
        )
    if args.svg is not None:
        save_concurrent_circles_static(
            output_path=args.svg,
            width=args.width,
            height=args.height,
            font_size=args.font_size,
            dpi=int(96 * args.scale),
            shared_region=args.shared_region,
            cluster_penalty=args.cluster_penalty,
            cluster_spread=args.cluster_spread,
            grid_step=args.grid_step,
            region_padding=args.region_padding,
            region_spacing=args.region_spacing,
            spacing_1way=args.spacing_1way,
            spacing_2way=args.spacing_2way,
            spacing_3way=args.spacing_3way,
            spacing_4way=args.spacing_4way,
        )


if __name__ == "__main__":
    main()


