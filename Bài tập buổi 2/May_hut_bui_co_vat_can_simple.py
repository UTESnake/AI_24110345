import random

def get_possible_moves(matrix, x, y):
    """
    Xác định các hướng đi có thể (né vật cản và biên ma trận)
    0: Sạch, 1: Bẩn, 2: Vật cản
    """
    m = len(matrix)       # Số hàng
    n = len(matrix[0])    # Số cột
    moves = []

    # Kiểm tra hướng Lên (Up)
    if x > 0 and matrix[x-1][y] != 2:
        moves.append("up")
        
    # Kiểm tra hướng Xuống (Down)
    if x < m - 1 and matrix[x+1][y] != 2:
        moves.append("down")
        
    # Kiểm tra hướng Trái (Left)
    if y > 0 and matrix[x][y-1] != 2:
        moves.append("left")
        
    # Kiểm tra hướng Phải (Right)
    if y < n - 1 and matrix[x][y+1] != 2:
        moves.append("right")
        
    return moves

def vacuum_agent_step(matrix, x, y):
    """
    Thực hiện 1 bước hành động của Agent tại vị trí (x, y)
    """
    state_value = matrix[x][y]
    print(f"Agent đang ở vị trí: ({x}, {y}), Trạng thái: {state_value}")

    # LUẬT 1: Nếu ô bẩn (1) -> Hút bụi
    if state_value == 1:
        print("-> Hành động: Hút bụi")
        matrix[x][y] = 0  # Chuyển trạng thái về sạch
    else:
        print("-> Hành động: Không (Ô đã sạch)")

    # LUẬT 2: Tìm đường đi tiếp theo
    possible_moves = get_possible_moves(matrix, x, y)
    
    if not possible_moves:
        print("-> Kết quả: Bị kẹt (Không có đường đi an toàn)")
        return x, y, "stop"

    # LUẬT 3: Chọn hướng đi ngẫu nhiên từ danh sách an toàn
    action = random.choice(possible_moves)
    print(f"-> Di chuyển tiếp theo: {action}")
    
    # Cập nhật tọa độ mới dựa trên hướng đã chọn
    new_x, new_y = x, y
    if action == "up": new_x -= 1
    elif action == "down": new_x += 1
    elif action == "left": new_y -= 1
    elif action == "right": new_y += 1
    
    return new_x, new_y, action


# Khởi tạo ma trận 3x3 giống ví dụ
# 0: Sạch, 1: Bẩn, 2: Vật cản
matrix = [
    [0, 0, 0],
    [0, 2, 0],
    [0, 0, 1]
]

# Đặt Agent bắt đầu tại vị trí có vết bẩn
x, y = 2, 2

print("MA TRẬN BAN ĐẦU:")
for row in matrix:
    print(row)

# Cho Agent chạy thử 3 bước
for step in range(1, 4):
    print(f"\n=== BƯỚC {step} ===")
    x, y, action = vacuum_agent_step(matrix, x, y)
    
    # In ra ma trận sau mỗi bước để dễ quan sát
    print("Ma trận hiện tại:")
    for row in matrix:
        print(row)
        
    if action == "stop":
        break