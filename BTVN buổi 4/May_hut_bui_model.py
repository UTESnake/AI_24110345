# 0 = Sạch | 1 = Bẩn | 2 = Vật cản | -1 = Chưa biết (bộ nhớ)

real_world = [
    [0, 1, 0],
    [1, 2, 0],
    [0, 0, 1]
]

agent_memory = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
]

# Vị trí ban đầu
x = 2
y = 2

step = 0
sucked = 0

def in_luoi(grid, agent_x, agent_y):
    for r in range(3):
        hang = []
        for c in range(3):
            if r == agent_x and c == agent_y:
                hang.append("A")
            else:
                hang.append(str(grid[r][c]))
        print("  " + str(hang))

print("(0=Sach, 1=Ban, 2=Vat can, A=Agent, -1=Chua biet)\n")
print("Môi trường ban đầu:")
in_luoi(real_world, x, y)

while step < 20:
    step = step + 1
    print(f"\n--- Bước {step} | Agent tại ({x},{y}) ---")

    current = real_world[x][y]
    print(f"  Cảm biến: {current}")

    agent_memory[x][y] = current

    # LUAT 1: Gap ban -> Hut
    if current == 1:
        print("  -> Hành động: HÚT BỤI")
        real_world[x][y] = 0
        agent_memory[x][y] = 0
        sucked = sucked + 1
        print("  Real world:")
        in_luoi(real_world, x, y)
        print("  Bộ nhớ:")
        in_luoi(agent_memory, x, y)
        continue

    # LUAT 2: Quet 4 huong
    all_dirs = [
        ["UP",   x - 1, y    ],
        ["DOWN", x + 1, y    ],
        ["LEFT",  x,     y - 1],
        ["RIGHT",  x,     y + 1]
    ]

    safe_moves = []
    unvisited  = []

    for i in range(4):
        name = all_dirs[i][0]
        nx   = all_dirs[i][1]
        ny   = all_dirs[i][2]

        if nx >= 0 and nx < 3 and ny >= 0 and ny < 3:
            neighbor = real_world[nx][ny]
            if neighbor == 2:
                agent_memory[nx][ny] = 2
            else:
                safe_moves.append([name, nx, ny])
                if agent_memory[nx][ny] == -1:
                    unvisited.append([name, nx, ny])

    # LUAT 3: Chon huong di
    if len(safe_moves) == 0:
        print("  -> Bị kẹt! DỪNG.")
        break

    if len(unvisited) > 0:
        chosen = unvisited[0]
        print(f"  -> Di chuyển {chosen[0]} tới ({chosen[1]},{chosen[2]}) [ô mới]")
    else:
        chosen = safe_moves[0]
        print(f"  -> Di chuyển {chosen[0]} tới ({chosen[1]},{chosen[2]}) [lùi lại]")

    x = chosen[1]
    y = chosen[2]

    print("  Real world:")
    in_luoi(real_world, x, y)
    print("  Bộ nhớ:")
    in_luoi(agent_memory, x, y)

    con_ban = False
    for r in range(3):
        for c in range(3):
            if real_world[r][c] == 1:
                con_ban = True

    if not con_ban:
        print("\nKhông còn ô bẩn! Hoàn tất.")
        break

print("\n=== Tổng kết ===")
print(f"Tổng số bước : {step}")
print(f"Số lần hút   : {sucked}")
print("\nSàn nhà hiện tại:")
in_luoi(real_world, -1, -1)
print("\nBộ nhớ agent:")
in_luoi(agent_memory, -1, -1)