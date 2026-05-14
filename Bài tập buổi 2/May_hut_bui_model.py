import random

def print_grid(grid, title):
    """Hàm in ma trận cho dễ nhìn"""
    print(f"--- {title} ---")
    for row in grid:
        # Thay thế số -1 (chưa biết) thành '?' cho dễ nhìn trong bộ nhớ
        print(["?" if cell == -1 else cell for cell in row])
    print()

def model_based_agent_step(real_grid, memory_grid, x, y):
    """
    Thực hiện 1 bước của Model-Based Agent
    0: Sạch, 1: Bẩn, 2: Vật cản, -1: Chưa khám phá (chỉ dùng cho memory)
    """
    m, n = len(real_grid), len(real_grid[0])
    
    # 1. NHẬN THỨC (Percept): Đọc trạng thái ô hiện tại
    current_status = real_grid[x][y]
    print(f"📍 Agent đang ở: ({x}, {y}) - Cảm biến thấy: {current_status}")
    
    # 2. CẬP NHẬT TRÍ NHỚ (Update State): Ghi nhớ ô này vào não
    memory_grid[x][y] = current_status
    
    # 3. LUẬT 1: Gặp bẩn thì Hút
    if current_status == 1:
        print("-> 🧹 Hành động: HÚT BỤI (SUCK)")
        real_grid[x][y] = 0        # Sàn nhà sạch
        memory_grid[x][y] = 0      # Não ghi nhớ sàn đã sạch
        return x, y, "SUCK"
        
    # 4. LUẬT 2: Sạch thì Quét cảm biến và Phân tích đường đi
    print("-> ✨ Ô hiện tại sạch. Quét cảm biến xung quanh...")
    safe_moves = []
    
    # Danh sách 4 hướng: (Tên hướng, Tọa độ X mới, Tọa độ Y mới)
    directions = [("up", x-1, y), ("down", x+1, y), ("left", x, y-1), ("right", x, y+1)]
    
    for move_name, nx, ny in directions:
        # Kiểm tra không đi ra ngoài viền
        if 0 <= nx < m and 0 <= ny < n:
            # Cảm biến nhìn sang ô bên cạnh
            neighbor_status = real_grid[nx][ny]
            
            # Ghi nhớ ngay nếu thấy vật cản
            if neighbor_status == 2:
                memory_grid[nx][ny] = 2
            # Nếu không phải vật cản, đưa vào danh sách an toàn
            else:
                safe_moves.append((move_name, nx, ny))
                
    if not safe_moves:
        print("-> 🚫 Kết quả: Bị kẹt! Không có đường đi.")
        return x, y, "STOP"

    # 5. LUẬT 3: Suy nghĩ và Ra quyết định (Dựa vào trí nhớ)
    unvisited_moves = []
    
    # Lọc ra những ô CÒN MỚI (chưa từng đi qua, trong bộ nhớ là -1)
    for move_name, nx, ny in safe_moves:
        if memory_grid[nx][ny] == -1: 
            unvisited_moves.append((move_name, nx, ny))
            
    # Ưu tiên khám phá chỗ mới để tiết kiệm pin
    if unvisited_moves:
        chosen = random.choice(unvisited_moves)
        print(f"-> 🧭 Quyết định: Ưu tiên khám phá ô mới đi {chosen[0].upper()}")
    else:
        # Xung quanh đều là ô đã quét sạch, đành phải đi lùi lại
        chosen = random.choice(safe_moves)
        print(f"-> 🔄 Quyết định: Đã dọn sạch quanh đây, lùi lại đi {chosen[0].upper()}")
        
    # Trả về tọa độ mới và hành động
    return chosen[1], chosen[2], chosen[0]

# ==========================================
# CHẠY THỬ NGHIỆM THUẬT TOÁN (MÔ PHỎNG 4 BƯỚC)
# ==========================================

# Môi trường thực tế
real_world = [
    [0, 0, 0],
    [0, 2, 0],
    [0, 0, 1]
]

# Bộ nhớ của Agent (Ban đầu chưa biết gì, gán là -1)
agent_memory = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
]

# Vị trí bắt đầu
x, y = 2, 2

print_grid(real_world, "MA TRẬN MÔI TRƯỜNG THỰC TẾ")

for step in range(1, 5):
    print(f"\n================ BƯỚC {step} ================")
    x, y, action = model_based_agent_step(real_world, agent_memory, x, y)
    
    if action == "STOP":
        break
        
print("\n================ TỔNG KẾT ================")
print_grid(real_world, "SÀN NHÀ HIỆN TẠI")
print_grid(agent_memory, "BẢN ĐỒ TRONG TRÍ NHỚ AGENT")