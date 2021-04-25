import time

"""
BeFS 
"""
# Giải thuật cho bài toán Sudoku
# Tối ưu thuật toán Backtracking dựa BeFS
# với heuristic là số lượng lựa chọn có thể có của một ô

# Class chứa data của một ô
# Giải thuật cho bài toán Sudoku
# Tối ưu thuật toán Backtracking dựa BeFS
# với heuristic là số lượng lựa chọn có thể có của một ô

# Class chứa data của một ô
class EntryData:
    def __init__(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

    def setData(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

def solve_sudoku_BeFS(matrix):
    cont = [True]
    # Kiểm tra xem bài toán có thể giải được hay không
    for row in range(9):
        for col in range(9):
            if not isCorrect(matrix, row, col):
                return
    sudoku_helper(matrix, cont)

def sudoku_helper(matrix, cont):
    if not cont[0]:
        return

    # Tìm ô có số lượng lựa chọn ( khả năng chọn số từ 1 - 9 ) ít nhất
    bestCell = EntryData(-1, -1, 100)
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:
                num_choices = count_choices(matrix, row, col)
                if bestCell.choices > num_choices:
                    bestCell.setData(row, col, num_choices)

    
    if bestCell.choices == 100: 
        cont[0] = False 
        return

    row = bestCell.row
    col = bestCell.col

    for value in range(1, 10):
        if not cont[0]:
            return

        matrix[row][col] = value

        if isCorrect(matrix, row, col):
            sudoku_helper(matrix, cont)

    if not cont[0]:
        return
    #Backtracking
    matrix[row][col] = 0 
            

# Đếm số lượng các số có thể điền vào trong ô có vị trí i,j (Tính heuristic)
def count_choices(matrix, i, j):
    canPick = [True,True,True,True,True,True,True,True,True,True] 
    
    for k in range(9):
        canPick[matrix[i][k]] = False

    for k in range(9):
        canPick[matrix[k][j]] = False

    r = i // 3
    c = j // 3
    for row in range(r*3, r*3+3):
        for col in range(c*3, c*3+3):
            canPick[matrix[row][col]] = False

    count = 0
    for value in range(1, 10): 
        if canPick[value]:
            count += 1

    return count

def isCorrect(matrix, row, col):
    for c in range(9):
        if matrix[row][col] != 0 and col != c and matrix[row][col] == matrix[row][c]:
            return False

    for r in range(9):
        if matrix[row][col] != 0 and row != r and matrix[row][col] == matrix[r][col]:
            return False

    r = row // 3
    c = col // 3
    for i in range(r*3, r*3+3):
        for j in range(c*3, c*3+3):
            if row != i and col != j and matrix[i][j] != 0 and matrix[i][j] == matrix[row][col]:
                return False
    
    return True

def isNonZero(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True

"""
Backtracking
"""

# hàm tìm kiếm xem giá trị có tồn tại trong hàng,
# cột hoặc khối không
def isValid(board, row, col, num):
    # nếu có trong hàng
    for i in range(9):
        if board[row][i] == num:
            return False
    #nếu có trong cột
    for i in range(9):
        if board[i][col] == num:
            return False
    #nếu có trong block
    c_row = row - row%3
    c_col = col - col%3
 
    for i in range(c_row, c_row+3):
        for j in range(c_col, c_col+3):
            if board[i][j] == num:
                return False
    #không tìm thấy            
    return True
 
def solveBoard(board, t0):
    if time.time() - t0 > 3:
        return False
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1,10):
                    if isValid(board, i, j, num):
                        board[i][j] = num
                        result = solveBoard(board, t0)
                        if result == True:
                            return True
                        else:
                            board[i][j] = 0
                return False
    return True
 
 # Biến trả về thứ nhất trả về ma trận kết quả
 # Thứ 2 trả về có giải được suduko không
def boardBackTracking(myBoard):
    t0 = time.time()
    if solveBoard(myBoard,t0)==False:
        return myBoard, False
    return myBoard, True
