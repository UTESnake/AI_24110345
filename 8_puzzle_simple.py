import random
import time

# Định nghĩa trạng thái đích để làm điều kiện cho Luật
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def INTERPRET_INPUT(percept):
    """
    Bước 1: Nhận thức thế cờ hiện tại
    """
    return tuple(percept)


def RULE_MATCH(state):
    """
    Bước 2: Hệ thống luật Condition-Action (Nếu - Thì)
    """
    # LUẬT 1 (Ưu tiên cao nhất): ĐÃ XẾP XONG -> DỪNG LẠI
    if state == GOAL_STATE:
        return "DONE", state

    # LUẬT 2: NẾU chưa xong -> Tìm các hướng có thể đi và chọn 1 hành động
    blank_idx = state.index(0)
    row, col = blank_idx // 3, blank_idx % 3

    valid_rules = []

    # Kích hoạt luật nếu điều kiện không gian cho phép
    if row > 0: valid_rules.append(("Lên", -1, 0))
    if row < 2: valid_rules.append(("Xuống", 1, 0))
    if col > 0: valid_rules.append(("Trái", 0, -1))
    if col < 2: valid_rules.append(("Phải", 0, 1))

    # Agent phản xạ: Bốc đại 1 hướng hợp lệ (do không có khả năng đánh giá tương lai)
    action_name, dr, dc = random.choice(valid_rules)

    new_row, new_col = row + dr, col + dc
    new_idx = new_row * 3 + new_col

    new_state = list(state)
    new_state[blank_idx], new_state[new_idx] = new_state[new_idx], new_state[blank_idx]

    return action_name, tuple(new_state)


def SIMPLE_REFLEX_AGENT(percept):
    """
    Hàm lõi đúng chuẩn:
    percept -> rút trích state -> so khớp rule -> trả về action
    """
    state = INTERPRET_INPUT(percept)

    # rule <- RULE-MATCH(state, rules)
    # action <- rule.ACTION
    action, next_state = RULE_MATCH(state)

    return action, next_state


def print_board(state):
    for i in range(0, 9, 3):
        row = [str(x) if x != 0 else ' ' for x in state[i:i + 3]]
        print(f"| {row[0]} | {row[1]} | {row[2]} |")
    print("-" * 13)


# ==========================================
# KHU VỰC CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    # Cho một bàn cờ CHỈ CÁCH ĐÍCH 1 BƯỚC để xem nó có biết dừng không
    start_state = (1, 2, 3,
                   4, 5, 6,
                   7, 0, 8)  # Ô trống nằm ở giữa hàng dưới cùng (chỉ cần đi Phải là thắng)

    current_state = start_state

    print("TRẠNG THÁI BẮT ĐẦU:")
    print_board(current_state)
    print("Agent bắt đầu phản xạ theo luật...\n")

    # Vẫn cho vòng lặp max 10 bước để phòng hờ nó đi bậy
    for step in range(1, 11):
        action, next_state = SIMPLE_REFLEX_AGENT(current_state)

        # Agent thực hiện hành động
        if action == "DONE":
            print(f"🎉 BƯỚC {step}: Cảm biến nhận diện bàn cờ đã khớp GOAL_STATE.")
            print("Luật 'Dừng lại' được kích hoạt. CHƯƠNG TRÌNH KẾT THÚC!")
            break

        print(f"Bước {step}: Phản xạ trượt ô '{action}'")
        current_state = next_state
        print_board(current_state)

        time.sleep(0.5)