# 1. Khai báo trạng thái bắt đầu và đích
start_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)
goal_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)

# 2. Khởi tạo hàng đợi và tập hợp reached 
frontier = [[start_state, []]]
reached = {start_state}

# Các bước di chuyển của ô số 0
moves = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

solution_path = None

# 3. THUẬT TOÁN TÌM KIẾM
while len(frontier) > 0:
    current = frontier.pop(0)
    state = current[0]
    path = current[1]

    if state == goal_state:
        solution_path = path
        break

    zero_idx = state.index(0)

    for action in moves:
        move_val = moves[action]
        new_idx = zero_idx + move_val

        if 0 <= new_idx <= 8:
            # Đang ở cột 0 (mép trái) thì cấm đi trái
            if action == 'LEFT' and zero_idx % 3 == 0:
                continue
            # Đang ở cột 2 (mép phải) thì cấm đi phải
            if action == 'RIGHT' and zero_idx % 3 == 2:
                continue
                
            new_state_list = list(state)
            new_state_list[zero_idx] = new_state_list[new_idx]
            new_state_list[new_idx] = 0
            new_state = tuple(new_state_list)

            if new_state not in reached:
                reached.add(new_state)
                new_path = list(path)
                new_path.append(action)
                frontier.append([new_state, new_path])

# ==========================================
# 4. CHẠY THỬ NGHIỆM VÀ IN KẾT QUẢ ĐÃ FORMAT
# ==========================================

print("--- KẾT QUẢ CHẠY THỬ NGHIỆM ---")

if solution_path is not None:
    print(f"Thành công! Cần {len(solution_path)} bước di chuyển để hoàn thành.\n")
    
    display_state = list(start_state)
    
    print("--- TRẠNG THÁI BẮT ĐẦU ---")
    print(f"[{display_state[0]}, {display_state[1]}, {display_state[2]}]")
    print(f"[{display_state[3]}, {display_state[4]}, {display_state[5]}]")
    print(f"[{display_state[6]}, {display_state[7]}, {display_state[8]}]")
    print()
    
    step_count = 1
    for action in solution_path:
        zero_idx = display_state.index(0)
        new_idx = zero_idx + moves[action]
        
        # Hoán đổi vị trí
        display_state[zero_idx] = display_state[new_idx]
        display_state[new_idx] = 0
        
        print(f"--- BƯỚC {step_count}: {action} ---")
        print(f"[{display_state[0]}, {display_state[1]}, {display_state[2]}]")
        print(f"[{display_state[3]}, {display_state[4]}, {display_state[5]}]")
        print(f"[{display_state[6]}, {display_state[7]}, {display_state[8]}]")
        print()
        
        step_count += 1
else:
    print("Thất bại! Không tìm thấy đường đi khả thi.")