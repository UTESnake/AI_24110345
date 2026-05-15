# Trạng thái đích (Goal State)
GOAL = [[1, 2, 3], 
        [4, 5, 6], 
        [7, 8, 0]]

class ModelBasedReflexAgent:
    def __init__(self):
        self.model = []  # Lưu lịch sử trạng thái

    def copy_matrix(self, matrix):
        new_matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(matrix[i][j])
            new_matrix.append(row)
        return new_matrix

    def update_state(self, percept):
        # 1. Tạo một bản sao của trạng thái hiện tại
        current_state_copy = self.copy_matrix(percept)
        
        # 2. Kiểm tra xem trạng thái này đã có trong lịch sử (model) chưa
        is_exist = False
        for saved_state in self.model:
            if saved_state == current_state_copy:
                is_exist = True
                
        # 3. Nếu chưa có thì lưu lại
        if is_exist == False:
            self.model.append(current_state_copy)
            
        return percept

    def get_manhattan(self, state):
        distance = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 0:
                    # Tìm tọa độ đích của giá trị 'val' bằng vòng lặp thay vì phép chia
                    target_r = 0
                    target_c = 0
                    for i in range(3):
                        for j in range(3):
                            if GOAL[i][j] == val:
                                target_r = i
                                target_c = j
                                
                    # Tính khoảng cách
                    distance += abs(r - target_r) + abs(c - target_c)
        return distance

    def rule_match(self, current_state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        best_action = None
        min_score = 999999 # Một số rất lớn

        # 1. Tìm vị trí ô trống (số 0) bằng vòng lặp for cơ bản
        r0 = 0
        c0 = 0
        for r in range(3):
            for c in range(3):
                if current_state[r][c] == 0:
                    r0 = r
                    c0 = c

        # 2. Thử từng hành động
        for action in possible_actions:
            new_r = r0
            new_c = c0
            
            if action == 'UP': 
                new_r = new_r - 1
            if action == 'DOWN': 
                new_r = new_r + 1
            if action == 'LEFT': 
                new_c = new_c - 1
            if action == 'RIGHT': 
                new_c = new_c + 1

            # Kiểm tra xem ô mới có nằm trong bảng không
            if new_r >= 0 and new_r <= 2 and new_c >= 0 and new_c <= 2:
                
                # Tạo trạng thái giả định bằng vòng lặp for
                temp_state = self.copy_matrix(current_state)
                
                # Đổi chỗ ô trống và ô bên cạnh
                temp_val = temp_state[new_r][new_c]
                temp_state[new_r][new_c] = temp_state[r0][c0]
                temp_state[r0][c0] = temp_val
                
                # Kiểm tra luật tránh lặp lại
                is_exist = False
                for saved_state in self.model:
                    if saved_state == temp_state:
                        is_exist = True
                
                # Nếu trạng thái này đã đi qua rồi thì bỏ qua (continue sang vòng lặp tiếp theo)
                if is_exist == True:
                    continue

                # Tính điểm Heuristic
                score = self.get_manhattan(temp_state)
                if score < min_score:
                    min_score = score
                    best_action = action
        
        return best_action

# --- CHẠY THỬ NGHIỆM ---
start_state = [[1, 2, 3], 
               [4, 0, 6], 
               [7, 5, 8]] 

agent = ModelBasedReflexAgent()

print("--- Bắt đầu chạy Agent ---")
current_percept = agent.copy_matrix(start_state)
steps = 0

while current_percept != GOAL and steps < 10:
    steps += 1
    
    state = agent.update_state(current_percept)
    action = agent.rule_match(state)
    
    if action == None:
        print("Agent bị kẹt hoặc không tìm thấy đường!")
        break
        
    print("Bước", steps, ": Trạng thái:", current_percept, "-> Hành động:", action)
    
    # Tìm lại ô trống để di chuyển thật trong môi trường
    r0 = 0
    c0 = 0
    for r in range(3):
        for c in range(3):
            if current_percept[r][c] == 0:
                r0 = r
                c0 = c
                
    # Thực hiện hành động
    if action == 'UP': 
        temp = current_percept[r0-1][c0]
        current_percept[r0-1][c0] = current_percept[r0][c0]
        current_percept[r0][c0] = temp
    if action == 'DOWN': 
        temp = current_percept[r0+1][c0]
        current_percept[r0+1][c0] = current_percept[r0][c0]
        current_percept[r0][c0] = temp
    if action == 'LEFT': 
        temp = current_percept[r0][c0-1]
        current_percept[r0][c0-1] = current_percept[r0][c0]
        current_percept[r0][c0] = temp
    if action == 'RIGHT': 
        temp = current_percept[r0][c0+1]
        current_percept[r0][c0+1] = current_percept[r0][c0]
        current_percept[r0][c0] = temp

if current_percept == GOAL:
    print("Bước cuối: Trạng thái:", current_percept, "-> ĐÃ TỚI ĐÍCH!")