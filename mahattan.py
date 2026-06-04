def input_matrix(rows, cols, name):
    """Hàm hỗ trợ nhập ma trận từ bàn phím"""
    print(f"--- Nhập ma trận {name} ({rows}x{cols}) ---")
    matrix = []
    for i in range(rows):
        while True:
            try:
                row_input = input(f"Nhập hàng {i+1} (gồm {cols} số cách nhau bởi dấu cách): ")
                row = list(map(int, row_input.split())) # Dùng int vì 8-Puzzle dùng số nguyên
                
                if len(row) != cols:
                    print(f"Lỗi: Vui lòng nhập đúng {cols} phần tử!")
                else:
                    matrix.append(row)
                    break
            except ValueError:
                print("Lỗi: Vui lòng chỉ nhập số!")
    return matrix

def calculate_8puzzle_manhattan(matrix_a, matrix_b):
    """Hàm tính khoảng cách Manhattan cho bài toán xếp số (bỏ qua số 0)"""
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    distance = 0
    
    # Bước 1: Lưu lại tọa độ đích của từng con số trong ma trận B
    # goal_positions sẽ có dạng: {giá_trị: (hàng, cột)}
    goal_positions = {}
    for r in range(rows):
        for c in range(cols):
            val = matrix_b[r][c]
            goal_positions[val] = (r, c)
            
    # Bước 2: Duyệt qua ma trận A, tính khoảng cách của từng số về vị trí đích
    for r in range(rows):
        for c in range(cols):
            val = matrix_a[r][c]
            
            # KHÔNG TÍNH KHOẢNG CÁCH CHO SỐ 0
            if val != 0:
                # Lấy tọa độ đích của số 'val' từ dictionary đã lưu
                goal_r, goal_c = goal_positions[val]
                
                # Cộng dồn khoảng cách: |hàng_hiện_tại - hàng_đích| + |cột_hiện_tại - cột_đích|
                distance += abs(r - goal_r) + abs(c - goal_c)
                
    return distance

def main():
    print("CHƯƠNG TRÌNH TÍNH KHOẢNG CÁCH MANHATTAN (8-PUZZLE)")
    try:
        rows = int(input("Nhập số hàng (n): "))
        cols = rows # Thường 8-Puzzle là ma trận vuông
        
        # Nhập 2 ma trận
        matrix_a = input_matrix(rows, cols, "A")
        matrix_b = input_matrix(rows, cols, "B")
        
        # Tính và in kết quả
        distance = calculate_8puzzle_manhattan(matrix_a, matrix_b)
        print(f"\n=> Khoảng cách Manhattan giữa ma trận A và B (bỏ qua số 0) là: {distance}")
        
    except ValueError:
        print("Lỗi: Vui lòng nhập số nguyên hợp lệ cho kích thước!")

if __name__ == "__main__":
    main()