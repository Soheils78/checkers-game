import tkinter as tk

# Constants for the game
BOARD_SIZE = 8
SQUARE_SIZE = 50
WHITE_piece = 'w'
RED_piece = 'r'
EMPTY = None
HIGHLIGHT_place = 'green'
current_player = RED_piece  # User starts as RED_piece


def assign_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                if row < 3:
                    board[row][col] = RED_piece
                elif row > 4:
                    board[row][col] = WHITE_piece
    return board


root = tk.Tk()
root.title("Checkers")
canvas = tk.Canvas(root, width=SQUARE_SIZE * BOARD_SIZE, height=SQUARE_SIZE * BOARD_SIZE)
canvas.pack()


def create_board(board):
    canvas.delete("all")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x0 = col * SQUARE_SIZE
            y0 = row * SQUARE_SIZE
            x1 = x0 + SQUARE_SIZE
            y1 = y0 + SQUARE_SIZE
            fill = "white" if (row + col) % 2 == 0 else "black"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            piece = board[row][col]
            if piece is not EMPTY and piece != HIGHLIGHT_place:
                color = "red" if piece.lower() == 'r' else "white"
                outline = "gold" if piece.isupper() else ""
                canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=color, outline=outline, width=6)
            elif piece == HIGHLIGHT_place:
                if highlight_checkboxv.get():
                    canvas.create_rectangle(x0, y0, x1, y1, fill=HIGHLIGHT_place, outline="")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='', outline="")


board = assign_board()
selected_piece = None


def check_for_within_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def creatieng_ai_moves(board):
    return creating_moves_for_color(board, WHITE_piece)  # WHITE_piece is the AI


def creating_player_moves(board):
    return creating_moves_for_color(board, RED_piece)  # RED_piece is the player


def creating_moves_for_color(board, color):
    all_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == color or board[row][col] == color.upper():
                piece_moves = available_moves(board, color, row, col)
                all_moves.extend(piece_moves)
    return all_moves


def available_moves(board, player_color, row, col):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if board[row][col].isupper() else \
        [(-1, -1), (-1, 1)] if player_color == WHITE_piece else [(1, -1), (1, 1)]
    capture_moves = []
    normal_moves = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if check_for_within_board(new_row, new_col):
            if board[new_row][new_col] == EMPTY:
                normal_moves.append(((row, col), (new_row, new_col), simulate_move(board, row, col, new_row, new_col)))
            elif board[new_row][new_col] not in [EMPTY, player_color, player_color.upper()] and board[new_row][
                new_col].lower() != player_color.lower():
                jump_row, jump_col = new_row + dr, new_col + dc
                if check_for_within_board(jump_row, jump_col) and board[jump_row][jump_col] == EMPTY:
                    capture_moves.append(
                        ((row, col), (jump_row, jump_col), simulate_move(board, row, col, jump_row, jump_col, True)))
    return capture_moves + normal_moves  # Prioritize capture moves


def simulate_move(board, start_row, start_col, end_row, end_col, is_capture=False):
    new_board = [row[:] for row in board]
    new_board[end_row][end_col] = new_board[start_row][start_col]  # Move piece to new location
    new_board[start_row][start_col] = EMPTY  # Clear the old location
    if is_capture:
        mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
        new_board[mid_row][mid_col] = EMPTY  # Remove the captured piece
    # Promote to King if reaching the opposite end
    if (end_row == 0 and new_board[end_row][end_col] == WHITE_piece) or (
            end_row == BOARD_SIZE - 1 and new_board[end_row][end_col] == RED_piece):
        new_board[end_row][end_col] = new_board[end_row][end_col].upper()
    return new_board


def duplicate_board(board):
    return [row[:] for row in board]


def interact_with_board(event):
    global current_player
    column = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE
    print(f"Clicked on row {row}, column {column}")

    piece = board[row][column]
    if piece is not None and piece.lower() == current_player:  # Check if the clicked piece belongs to the current player
        if (current_player == RED_piece and piece.islower()) or (
                current_player == WHITE_piece and piece.islower()) or piece.isupper():
            highlight_moves(row, column)
        else:
            print("It's not your piece!")
    elif piece == HIGHLIGHT_place:
        move_piece(row, column)
    else:
        print("Not your turn or invalid move.")


def highlight_moves(row, col):
    global selected_piece
    selected_piece = (row, col)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == HIGHLIGHT_place:
                board[r][c] = EMPTY
    player_color = board[row][col]
    possible_moves_list = available_moves(board, player_color, row, col)
    for _, (new_row, new_col), _ in possible_moves_list:
        board[new_row][new_col] = HIGHLIGHT_place
    create_board(board)


def check_for_win():
    white_count = 0
    black_count = 0
    for row in board:
        for piece in row:
            if piece in [WHITE_piece, WHITE_piece.upper()]:
                white_count += 1
            elif piece in [RED_piece, RED_piece.upper()]:
                black_count += 1

    win_text_id = None
    if white_count == 0:
        win_text_id = canvas.create_text(SQUARE_SIZE * BOARD_SIZE // 2, SQUARE_SIZE * BOARD_SIZE // 2,
                                         text="Black wins!", font=('Arial', 28, 'bold'), fill="blue")
        return True
    elif black_count == 0:
        win_text_id = canvas.create_text(SQUARE_SIZE * BOARD_SIZE // 2, SQUARE_SIZE * BOARD_SIZE // 2,
                                         text="White wins!", font=('Arial', 28, 'bold'), fill="blue")
        return True
    return False


def move_piece(row, col):
    global selected_piece, current_player, board  # Declare board as global
    sr, sc = selected_piece
    mid_row, mid_col = (sr + row) // 2, (sc + col) // 2
    captured_piece = board[mid_row][mid_col]  # Get the captured piece, if any

    board[sr][sc], board[row][col] = EMPTY, board[sr][sc]  # Move the piece
    # Check for making a king if reaching the last row
    if ((current_player == RED_piece and row == BOARD_SIZE - 1)
            or (current_player == WHITE_piece and row == 0)):
        board[row][col] = board[row][col].upper()  # King the piece

    if abs(row - sr) == 2:  # If it was a capture move
        board[mid_row][mid_col] = EMPTY  # Remove the captured piece
        # Check if the captured piece is a king, crown the capturing piece immediately
        if captured_piece.isupper():
            board[row][col] = board[row][col].upper()

    # Clear highlights after move
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == HIGHLIGHT_place:
                board[r][c] = EMPTY

    selected_piece = None
    create_board(board)
    root.update()
    # Check if the game is won after the move
    if check_for_win():  # Check for win after the move
        canvas.unbind("<Button-1>")  # Disable further clicks
    # Switch turns only after a move is made
    current_player = WHITE_piece if current_player == RED_piece else RED_piece
    if current_player == WHITE_piece:
        ai()


def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            if piece:
                if piece == WHITE_piece:
                    score += 1
                elif piece == WHITE_piece.upper():  # White king
                    score += 2
                elif piece == RED_piece:
                    score -= 1
                elif piece == RED_piece.upper():  # Black king
                    score -= 2
    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(board)
    if maximizing_player:
        max_eval = float('-inf')
        for _, _, child in creatieng_ai_moves(board):
            evaluation = minimax(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for _, _, child in creating_player_moves(board):
            evaluation = minimax(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval


def ai():
    global board, current_player  # Declare board and current_player as global
    best_score = float('-inf')
    best_move = None
    current_depth = (ai_depth.get() * 2)
    for start_pos, end_pos, new_board in creatieng_ai_moves(board):
        score = minimax(new_board, current_depth, float('-inf'), float('inf'), False)
        if abs(start_pos[0] - end_pos[0]) == 2:
            score += 10  # Add a bonus for capture moves
        if score > best_score:
            best_score = score
            best_move = (start_pos, end_pos, new_board)
    if best_move:
        _, _, best_board = best_move
        board = best_board  # Update the global board state
        create_board(board)
        if check_for_win():
            canvas.unbind("<Button-1>")  # Disable further clicks
        else:
            current_player = RED_piece


def new_game():
    global board, current_player
    canvas.delete("all")  # Clear the canvas including any text
    board = assign_board()  # Reinitialize the board
    current_player = RED_piece  # Reset current player to start
    create_board(board)  # Redraw the board
    print("New game started. It's RED_piece's turn.")


def instructions():
    instructions_window = tk.Toplevel(root)
    instructions_window.title("instructions")
    instructions_window_text = """instructions_window


    -The red pieces are the user pieces and the white pieces are AI pieces. 

    -The slider can change the level of the difficulty. 

    -The new game button is for reset the game. 

    -Each piece when reach to the last row, then it will become king.

    -If the normal piece capture the king piece, then that normal piece will become to the king. 
    """
    tk.Label(instructions_window, text=instructions_window_text, justify=tk.LEFT, padx=10, pady=10).pack()
    close_button = tk.Button(instructions_window, text="Close", command=instructions_window.destroy)
    close_button.pack(pady=5)


def show_rules():
    rules_window = tk.Toplevel(root)
    rules_window.title("Checkers Rules")
    rules_text = """Game Rules:
1. Pieces move diagonally.
2. If the adjacent square contains an opponent's piece, and the square immediately beyond it is vacant, the opponent's piece may be captured.
3. Kings can move both forward and backward.
4. The game ends when one player captures all the opponent's pieces or blocks all possible moves."""
    tk.Label(rules_window, text=rules_text, justify=tk.LEFT, padx=10, pady=10).pack()
    close_button = tk.Button(rules_window, text="Close", command=rules_window.destroy)
    close_button.pack(pady=5)


rules_button = tk.Button(root, text="Show Rules", command=show_rules)
rules_button.pack(side=tk.TOP, anchor='e')  # Top right corner

instructions_button = tk.Button(root, text="instructions", command=instructions)
instructions_button.pack(side=tk.BOTTOM, anchor='e')

# Initialize the AI depth variable
ai_depth = tk.IntVar(value=1)  # Default depth

# Create a scale for selecting AI depth
ai_depth_scale = tk.Scale(root, from_=1, to=3, variable=ai_depth, orient=tk.HORIZONTAL, label="Difficulty", length=100)
ai_depth_scale.pack(side=tk.BOTTOM)

highlight_checkboxv = tk.BooleanVar(value=1)
highlight_checkbox = tk.Checkbutton(root, text="possible moves of piece", variable=highlight_checkboxv)
highlight_checkbox.pack(side=tk.TOP, anchor='w')  # Top left corner

canvas.bind("<Button-1>", interact_with_board)
board = assign_board()
create_board(board)

reset_button = tk.Button(root, text="New Game", command=new_game)
reset_button.pack(side=tk.RIGHT)

root.mainloop()