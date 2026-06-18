from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from csp import solve
from render import draw
from utils import load_graph, load_regions


def parse_args():
    parser = argparse.ArgumentParser(description="HCMC map coloring with backtracking")
    parser.add_argument("--delay", type=float, default=0.12, help="Delay mỗi bước")
    parser.add_argument(
        "--no-animation",
        action="store_true",
        help="Chỉ vẽ kết quả cuối cùng",
    )
    parser.add_argument(
        "--output",
        default="output/hcm_map_coloring.png",
        help="Đường dẫn ảnh kết quả",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    regions = load_regions()
    graph = load_graph(regions)
    assignment, trace = solve(graph)

    fig, ax = plt.subplots(figsize=(11, 9))
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.95)
    fig.suptitle("HCMC Map Coloring - Backtracking Animation", fontsize=15)

    # Phóng to cửa sổ ngay khi chạy nhưng vẫn giữ thanh tiêu đề và nút X.
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state("zoomed")  # TkAgg trên Windows
    except (AttributeError, TypeError):
        try:
            manager.window.showMaximized()  # Qt backend
        except AttributeError:
            pass

    if not args.no_animation:
        draw(ax, regions, {})
        plt.pause(0.8)

        current = {}
        status = None
        for action, node, color in trace:
            if action == "assign":
                current[node] = color
            elif action == "unassign":
                current.pop(node, None)

            status = (action, node, color)
            draw(ax, regions, current, status)
            # Giữ bước quay lui lâu hơn để người xem nhận ra nhánh bị hủy.
            pause = args.delay * 3 if action == "unassign" else args.delay
            plt.pause(pause)

    last_node = next(reversed(assignment))
    draw(ax, regions, assignment, ("done", last_node, assignment[last_node]))

    backtrack_count = sum(action == "unassign" for action, _, _ in trace)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150, bbox_inches="tight", facecolor="white")
    print("Ket qua mau:", assignment)
    print("So lan quay lui:", backtrack_count)
    print("Da luu:", output.resolve())

    # plt.pause() trong phần animation bật chế độ hiển thị không chặn.
    # Tắt interactive mode và chờ người dùng tự đóng cửa sổ kết quả.
    plt.ioff()
    if plt.get_backend().lower() == "agg":
        plt.close(fig)
    else:
        plt.show(block=True)


if __name__ == "__main__":
    main()
