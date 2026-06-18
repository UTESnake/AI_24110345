from __future__ import annotations

from pathlib import Path

import matplotlib.patheffects as path_effects
import rasterio


COLOR_MAP = {
    "red": "#ff4d4d",
    "green": "#42ef82",
    "blue": "#4da6ff",
    "yellow": "#ffd84d",
}

COLOR_NAMES = {
    "red": "Do",
    "green": "Xanh la",
    "blue": "Xanh duong",
    "yellow": "Vang",
}

BASEMAP_FILE = Path(__file__).with_name("data") / "hcm_basemap.tif"


def _draw_basemap(ax):
    ax.set_facecolor("#dddddd")
    if not BASEMAP_FILE.exists():
        return

    with rasterio.open(BASEMAP_FILE) as source:
        rgb = source.read([1, 2, 3]).astype(float)
        gray = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
        bounds = source.bounds

    ax.imshow(
        gray,
        cmap="gray",
        vmin=0,
        vmax=255,
        extent=(bounds.left, bounds.right, bounds.bottom, bounds.top),
        origin="upper",
        zorder=0,
    )


def draw(ax, regions, assignment, status=None):
    ax.clear()
    _draw_basemap(ax)

    min_x, min_y, max_x, max_y = regions.total_bounds
    pad_x = (max_x - min_x) * 0.08
    pad_y = (max_y - min_y) * 0.035

    for row in regions.itertuples():
        assigned_color = assignment.get(row.name)
        facecolor = COLOR_MAP.get(assigned_color, "#a8a8a8")
        alpha = 0.74 if assigned_color else 0.28

        regions.loc[[row.Index]].plot(
            ax=ax,
            facecolor=facecolor,
            edgecolor="#181818",
            linewidth=1.35,
            alpha=alpha,
            zorder=2,
        )

        point = row.geometry.representative_point()
        label = ax.text(
            point.x,
            point.y,
            row.name,
            ha="center",
            va="center",
            fontsize=8.5,
            weight="bold",
            color="white" if assigned_color else "#333333",
            zorder=3,
        )
        if assigned_color:
            label.set_path_effects(
                [path_effects.withStroke(linewidth=2, foreground="#33333388")]
            )

    ax.set_xlim(min_x - pad_x, max_x + pad_x)
    ax.set_ylim(min_y - pad_y, max_y + pad_y)
    ax.set_aspect("equal")
    ax.set_axis_off()

    if status:
        action, node, color = status
        messages = {
            "try": f"Thu mau: {node} = {COLOR_NAMES[color]}",
            "reject": f"Xung dot: {node} khong the dung {COLOR_NAMES[color]}",
            "assign": f"Gan mau: {node} = {COLOR_NAMES[color]}",
            "unassign": f"QUAY LUI: bo mau {COLOR_NAMES[color]} cua {node}",
            "done": f"Hoan tat: {node} = {COLOR_NAMES[color]}",
        }
        box_color = {
            "try": "#fff7d6",
            "reject": "#ffd6d6",
            "assign": "#dcfce7",
            "unassign": "#ffe4b5",
            "done": "white",
        }
        ax.text(
            0.015,
            0.975,
            messages[action],
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=13,
            weight="bold" if action == "unassign" else "normal",
            color="black",
            bbox={
                "boxstyle": "round,pad=0.3",
                "facecolor": box_color[action],
                "edgecolor": "#555555",
                "alpha": 0.92,
            },
            zorder=5,
        )
