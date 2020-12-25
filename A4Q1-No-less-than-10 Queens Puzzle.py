import sys

def fourteen_queen(curr_row, columns, left, right, chess):
    global COUNT, N_QUEENS

    # all queens are placed
    if curr_row == N_QUEENS:
        COUNT+=1
        return

    if chess[curr_row]:
        # try column i
        for i in chess[curr_row]:

            l = i - curr_row + 13
            r = i + curr_row

            # check columns and diagonals
            if columns[i] == 0 and left[l] == 0 and right[r] == 0:

                columns[i], left[l], right[r] = 1, 1, 1
                fourteen_queen(curr_row + 1, columns, left, right, chess)

                # backtracking
                columns[i], left[l], right[r] = 0, 0, 0

    else:
        # rows that are already filled with queens at the beginning
        fourteen_queen(curr_row + 1, columns, left, right, chess)


num_case = int(sys.stdin.readline())
N_QUEENS = 14
for _ in range(num_case):
    s = sys.stdin.readline().split()

    COUNT = 0
    board = [set() for i in range(N_QUEENS)]
    cols, known_row = [0] * N_QUEENS, [0] * N_QUEENS
    left_diag, right_diag = [0] * (2*N_QUEENS-1), [0] * (2*N_QUEENS-1)

    for i in range(len(s) // 2):
        row, col = int(s[2*i])-1, int(s[2*i+1])-1
        known_row[row] = 1
        cols[col] = 1
        left_diag[col - row + 13] = 1
        right_diag[col + row] = 1

    # take away impossible positions according to existing queens
    for r in range(N_QUEENS):
        if not known_row[r]:
            for c in range(N_QUEENS):
                if cols[c] == 0 and left_diag[c-r+13] == 0 and right_diag[c+r] == 0:
                    board[r].add(c)

    fourteen_queen(0, cols, left_diag, right_diag, board)
    print(COUNT)

