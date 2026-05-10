import random

M = 3  # Số hàng (từ 0 đến M-1)
N = 3  # Số cột (từ 0 đến N-1)

def possible_move(x, y): 
    move = []
    if x > 0:
        move.append('up')  # Chưa đụng trần -> được đi Lên
    if x < M - 1:
        move.append('down')  # Chưa đụng đáy -> được đi Xuống
    if y > 0:
        move.append('left')  # Chưa đụng tường trái -> được đi Trái
    if y < N - 1:
        move.append('right')  # Chưa đụng tường phải -> được đi Phải
    return move

def RULE_MATCH(state_value, x, y):
  
    if state_value == 0:
        moves = possible_move(x, y)
        action = random.choice(moves)
        return action, state_value

    elif state_value == 1:
        state_value = 0
        action = 'suck'
        return action, state_value


def SIMPLE_REFLEX_AGENT(percept):
    x, y, state_value = percept
    action, new_state_value = RULE_MATCH(state_value, x, y)
    return action, new_state_value

if __name__ == "__main__":

    # TH1: Robot đang ở góc dưới cùng bên phải (x=2, y=2) và sàn SẠCH (0)
    # Kỳ vọng: Hàm possible_move chỉ trả về ['up', 'left']
    percept_1 = (2, 2, 0)
    act_1, new_state_1 = SIMPLE_REFLEX_AGENT(percept_1)
    print(f"Nhận thức 1: Tọa độ (2,2), Trạng thái: {percept_1[2]}")
    print(f"-> Hành động: {act_1} (Trạng thái sau đó: {new_state_1})\n")

    # TH2: Robot đang ở giữa phòng (x=1, y=1) và sàn BẨN (1)
    # Kỳ vọng: Đổi state thành 0 và Hút
    percept_2 = (1, 1, 1)
    act_2, new_state_2 = SIMPLE_REFLEX_AGENT(percept_2)
    print(f"Nhận thức 2: Tọa độ (1,1), Trạng thái: {percept_2[2]}")
    print(f"-> Hành động: {act_2} (Trạng thái đã được làm sạch thành: {new_state_2})")