def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    if len(l) == 0:
        return []
    left = 0
    right = len(l) - 1
    while left < right:
        l[left], l[right] = l[right], l[left]
        left += 1
        right -= 1
    return l
 
def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.
    The board must be completed so that every row, column, and 3x3 section
    contains all digits from 1 to 9.
    Input: a 9x9 matrix representing the board.
    """
    def dfs(matrix, x, y):
        nextY = 0 if y == 8 else y + 1
        nextX = x + 1 if nextY == 0 else x
        
        if x == 9 and y == 0:
            return True
        
        if matrix[x][y] != 0:
            return dfs(matrix, nextX, nextY)
        else:
            for i in range(1, 10):
                matrix[x][y] = i
                if not check(matrix, x, y, i):
                    continue
                if dfs(matrix, nextX, nextY):
                    return True
            matrix[x][y] = 0
            return False
    
    def check(matrix, curX, curY, curNum):
        for j in range(9):
            if j == curY:
                continue
            if matrix[curX][j] == curNum:
                return False
        
        for i in range(9):
            if i == curX:
                continue
            if matrix[i][curY] == curNum:
                return False
        
        box_start_row = curX // 3 * 3
        box_start_col = curY // 3 * 3
        for i in range(3):
            for j in range(3):
                row = box_start_row + i
                col = box_start_col + j
                if row != curX and col != curY and matrix[row][col] == curNum:
                    return False
        
        return True

    dfs(matrix, 0, 0)
    return matrix
