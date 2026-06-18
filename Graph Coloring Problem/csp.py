COLORS = ["green", "red", "blue", "yellow"]

# Thứ tự cố định phục vụ minh họa: với thứ tự này thuật toán sẽ đi vào một
# vài ngõ cụt và phải quay lui thật sự trước khi tìm thấy nghiệm.
BACKTRACKING_ORDER = [
    "Tan Phu",
    "Binh Tan",
    "Hoc Mon",
    "Q7",
    "Q8",
    "Q6",
    "Go Vap",
    "Q3",
    "Tan Binh",
    "Can Gio",
    "Phu Nhuan",
    "Binh Chanh",
    "Q4",
    "Nha Be",
    "Q11",
    "Q10",
    "Q5",
    "Q1",
    "Q12",
    "Thu Duc",
    "Binh Thanh",
    "Cu Chi",
]


def solve(graph):
    """Tô màu bằng chronological backtracking thuần, không forward checking."""
    assignment = {}
    trace = []
    nodes = [node for node in BACKTRACKING_ORDER if node in graph]
    nodes.extend(node for node in graph if node not in nodes)

    def safe(node, color):
        # Chỉ nhìn các đỉnh đã được gán màu. Không cắt miền màu hay dự đoán
        # cho các đỉnh chưa xét (không dùng forward checking).
        return all(assignment.get(neighbor) != color for neighbor in graph[node])

    def backtrack(index=0):
        if index == len(nodes):
            return True

        node = nodes[index]
        for color in COLORS:
            trace.append(("try", node, color))

            if not safe(node, color):
                trace.append(("reject", node, color))
                continue

            assignment[node] = color
            trace.append(("assign", node, color))

            if backtrack(index + 1):
                return True

            # Nhánh phía sau thất bại: xóa phép gán gần nhất rồi thử màu khác.
            trace.append(("unassign", node, color))
            del assignment[node]

        return False

    if not backtrack():
        raise RuntimeError("Không tìm được phương án tô màu hợp lệ.")
    return assignment.copy(), trace
