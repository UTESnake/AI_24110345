# ============================================================
# MODEL-BASED REFLECT AGENT - MÁY HÚT BỤI
# Theo pseudocode: UPDATE_STATE -> RULE_MATCH -> ACTION
# ============================================================
# 0 = Sach | 1 = Ban | -1 = Chua biet (bo nho)

real_world = [
    [1, 0, 0],
    [0, 0, 0],
    [0, 1, 1]
]

# ---- PERSISTENT (bo nho agent giu giua cac buoc) ----
state  = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]  # trang thai moi truong
model  = []   # lich su (vi_tri, hanh_dong) da thuc hien
action = None # hanh dong truoc do

# ---- TAP LUAT (rules) ----
# Rule 1: state_value = 1  ->  action = SUCK,  state_value = 0
# Rule 2: state_value = 0  ->  action = possible_move(x, y)

def possible_move(x, y, m, n):
    """Tra ve danh sach huong co the di (khong ra ngoai luoi)"""
    moves = []
    if x > 0:     moves.append("up")
    if x < m - 1: moves.append("down")
    if y > 0:     moves.append("left")
    if y < n - 1: moves.append("right")
    return moves

def rule_match(state_value, x, y, m, n):
    """
    RULE_MATCH: khop trang thai voi tap luat, tra ve action
    Rule 1: Ban -> SUCK
    Rule 2: Sach -> chon huong di tu possible_move
    """
    if state_value == 1:
        return "SUCK"
    if state_value == 0:
        moves = possible_move(x, y, m, n)
        if len(moves) == 0:
            return "STOP"
        # Uu tien o chua tham
        for move in moves:
            nx, ny = x, y
            if move == "up":    nx = x - 1
            if move == "down":  nx = x + 1
            if move == "left":  ny = y - 1
            if move == "right": ny = y + 1
            if state[nx][ny] == -1:
                return move
        # Khong co o moi -> di o dau tien con lai
        return moves[0]
    return "STOP"

def update_state(state, x, y, action, percept, model):
    """
    UPDATE_STATE: cap nhat bo nho dua vao
    - action: hanh dong vua thuc hien
    - percept: cam bien hien tai
    - model: lich su vi tri & hanh dong
    """
    state[x][y] = percept
    model.append((x, y, action))
    return state

def in_luoi(grid, ax, ay, title):
    print(f"  {title}:")
    for r in range(len(grid)):
        hang = []
        for c in range(len(grid[r])):
            if r == ax and c == ay:
                hang.append("A")
            else:
                hang.append(str(grid[r][c]))
        print("  ", hang)

# ============================================================
# CHAY THUAT TOAN
# ============================================================
m = len(real_world)
n = len(real_world[0])

x, y = 2, 2   # vi tri bat dau
step  = 0
sucked = 0
dung  = False

print("=== BAT DAU MO PHONG ===")
print("(0=Sach, 1=Ban, A=Agent, -1=Chua biet)\n")
print("Moi truong ban dau:")
in_luoi(real_world, x, y, "real_world")

while not dung:
    step += 1
    print(f"\n========== BUOC {step} ==========")

    # 1. PERCEPT: doc cam bien
    percept = real_world[x][y]
    print(f"  percept ({x},{y}) = {percept}")

    # 2. UPDATE_STATE
    state = update_state(state, x, y, action, percept, model)
    print(f"  state_value tai ({x},{y}) = {state[x][y]}")

    # 3. RULE_MATCH -> lay action
    action = rule_match(state[x][y], x, y, m, n)
    print(f"  action = {action}")

    # 4. THUC HIEN action
    if action == "SUCK":
        real_world[x][y] = 0
        state[x][y] = 0
        sucked += 1
        print(f"  -> HUT BUI tai ({x},{y}), state_value = 0")

    elif action == "STOP":
        print("  -> Bi ket! DUNG.")
        dung = True

    else:
        # Di chuyen
        if action == "up":    x = x - 1
        if action == "down":  x = x + 1
        if action == "left":  y = y - 1
        if action == "right": y = y + 1
        print(f"  -> Di chuyen {action.upper()} toi ({x},{y})")

    in_luoi(real_world, x, y, "real_world")
    in_luoi(state,      x, y, "state (bo nho)")

    # Kiem tra dieu kien dung: het o ban
    con_ban = False
    for r in range(m):
        for c in range(n):
            if real_world[r][c] == 1:
                con_ban = True

    if not con_ban:
        print("\n  Khong con o ban! Hoan tat.")
        dung = True

# ============================================================
print("\n=== TONG KET ===")
print(f"Tong buoc : {step}")
print(f"So lan hut: {sucked}")
print(f"Lich su model (vi_tri, hanh_dong):")
for item in model:
    print(f"  ({item[0]},{item[1]}) -> {item[2]}")