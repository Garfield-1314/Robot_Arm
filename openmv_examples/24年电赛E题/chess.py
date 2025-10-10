# chess.py
SIZE = 3

# 检查赢了吗
def check_win(board, player):
    # Check rows and columns
    for i in range(SIZE):
        if all(board[i][j] == player for j in range(SIZE)) or \
           all(board[j][i] == player for j in range(SIZE)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(SIZE)) or \
       all(board[i][SIZE - 1 - i] == player for i in range(SIZE)):
        return True
    return False

# 检查平局了吗
def check_draw(board):
    return all(board[i][j] != ' ' for i in range(SIZE) for j in range(SIZE))


# 计算策略得分
def minimax(board, depth, is_maximizing):
    computer = 'X'
    player = 'O'

    if check_win(board, computer):
        return 10 - depth
    if check_win(board, player):
        return depth - 10
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == ' ':
                    board[i][j] = computer
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score


# 计算下一步位置
def computer_move(board):
    if board == [
        [" "," "," "],
        [" "," "," "],
        [" "," "," "]
    ]:
        return 1,1
    best_score = float('-inf')
    move = (-1, -1)
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move != (-1, -1):
        # board[move[0]][move[1]] = 'X'
        print(f"Computer places X at ({move[0]}, {move[1]})")
        return move[0], move[1]


# 检查该谁走了
def check_turn(board):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return "X" if x_count == o_count else "O"