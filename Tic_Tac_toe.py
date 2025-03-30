import random
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font

# Initialize the main app
root = Tk()
root.title("Tic Tac Toe")
root.geometry("1000x700")
root.resizable(False, False)

# Create a custom style
style = ttk.Style()
style.configure("TButton", font=("Arial", 12))
style.configure("TLabel", font=("Arial", 12))
style.configure("Title.TLabel", font=("Arial", 24, "bold"))
style.configure("Header.TLabel", font=("Arial", 18, "bold"))
style.configure("Status.TLabel", font=("Arial", 14))

# Game state variables
clicked = True  # X starts first
count = 0
mode = None  # To determine the selected mode (AI or friend)
player1_name = "Player 1"
player2_name = "Player 2"
player1_symbol = "X"
player2_symbol = "O"
buttons = []  # To store button references
ai_difficulty = "medium"  # Default AI difficulty

# Color themes
themes = {
    "light": {
        "bg": "#f0f0f0",
        "button_bg": "#ffffff",
        "button_active_bg": "#e0e0e0",
        "button_fg": "#000000",
        "x_color": "#2196F3",  # Blue
        "o_color": "#F44336",  # Red
        "win_color": "#4CAF50",  # Green
        "frame_bg": "#e0e0e0",
        "highlight_bg": "#bbdefb"
    },
    "dark": {
        "bg": "#303030",
        "button_bg": "#424242",
        "button_active_bg": "#616161",
        "button_fg": "#ffffff",
        "x_color": "#64B5F6",  # Light Blue
        "o_color": "#EF5350",  # Light Red
        "win_color": "#66BB6A",  # Light Green
        "frame_bg": "#424242",
        "highlight_bg": "#1976D2"
    }
}

# Current theme
current_theme = "light"
theme = themes[current_theme]

# Configure root background
root.configure(bg=theme["bg"])

# Disable all buttons (used after game ends)
def disable_all_buttons():
    for button in buttons:
        button.config(state=DISABLED)

# Check if someone won
def checkifwon():
    global clicked, count
    Winner = False

    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]

    for combo in win_combinations:
        if (buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"]) and buttons[combo[0]]["text"] != " ":
            Winner = True
            for idx in combo:
                buttons[idx].config(bg=theme["win_color"], fg="white")
            winner_name = player1_name if buttons[combo[0]]["text"] == player1_symbol else player2_name
            messagebox.showinfo("Tic Tac Toe", f"Congrats! {winner_name} has won!")
            disable_all_buttons()
            return

    # Check for tie
    if count == 9 and not Winner:
        messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        disable_all_buttons()
        # Show restart button when game is a tie
        show_restart_button()

# Show restart button when the game is a tie
def show_restart_button():
    restart_btn = Button(tie_button_frame, text="Restart Game", font=("Arial", 12), 
                         bg=theme["button_bg"], fg=theme["button_fg"], 
                         activebackground=theme["button_active_bg"],
                         padx=15, pady=8, bd=0,
                         command=reset)
    restart_btn.pack(pady=10)
    tie_button_frame.pack(fill=X, pady=10)

# Helper function to check for winning combinations
def check_winning(board, symbol):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == symbol:
            return True
    return False

# Minimax algorithm for "hard" AI difficulty
def minimax(board, is_maximizing):
    # Check for terminal states
    if check_winning(board, player2_symbol):
        return 1  # AI win
    elif check_winning(board, player1_symbol):
        return -1  # Human win
    elif " " not in board:
        return 0  # Tie

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = player2_symbol
                score = minimax(board, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = player1_symbol
                score = minimax(board, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

# AI logic for making a move
def ai_move():
    global count, clicked, ai_difficulty
    empty_buttons = [idx for idx, button in enumerate(buttons) if button["text"] == " "]
    
    if not empty_buttons:
        return  # No moves available
        
    board_state = [button["text"] for button in buttons]
    
    if ai_difficulty == "easy":
        # AI picks a random empty cell
        choice = random.choice(empty_buttons)
        buttons[choice]["text"] = player2_symbol
        buttons[choice].config(fg=theme["o_color"])
    
    elif ai_difficulty == "medium":
        # Try to win first
        for idx in empty_buttons:
            board_state[idx] = player2_symbol
            if check_winning(board_state, player2_symbol):
                buttons[idx]["text"] = player2_symbol
                buttons[idx].config(fg=theme["o_color"])
                clicked = True
                count += 1
                update_turn_label()
                checkifwon()
                return
            board_state[idx] = " "
        
        # Block player if they're about to win
        for idx in empty_buttons:
            board_state[idx] = player1_symbol
            if check_winning(board_state, player1_symbol):
                buttons[idx]["text"] = player2_symbol
                buttons[idx].config(fg=theme["o_color"])
                clicked = True
                count += 1
                update_turn_label()
                checkifwon()
                return
            board_state[idx] = " "
        
        # Take center if available
        if 4 in empty_buttons:
            buttons[4]["text"] = player2_symbol
            buttons[4].config(fg=theme["o_color"])
        else:
            # Random move if no strategic moves
            choice = random.choice(empty_buttons)
            buttons[choice]["text"] = player2_symbol
            buttons[choice].config(fg=theme["o_color"])
    
    elif ai_difficulty == "hard":
        # Minimax algorithm
        best_score = -float("inf")
        best_move = None
        
        for idx in empty_buttons:
            board_state[idx] = player2_symbol
            score = minimax(board_state, False)
            board_state[idx] = " "
            if score > best_score:
                best_score = score
                best_move = idx
        
        if best_move is not None:
            buttons[best_move]["text"] = player2_symbol
            buttons[best_move].config(fg=theme["o_color"])
        else:
            # Fallback to random move
            choice = random.choice(empty_buttons)
            buttons[choice]["text"] = player2_symbol
            buttons[choice].config(fg=theme["o_color"])

    clicked = True
    count += 1
    update_turn_label()
    checkifwon()

# Button click event
def b_click(button_idx):
    global clicked, count
    button = buttons[button_idx]
    if button["text"] == " ":
        if clicked:
            button["text"] = player1_symbol
            button.config(fg=theme["x_color"])
            clicked = False
            count += 1
            update_turn_label()
            checkifwon()
            if mode == "ai" and count < 9 and not clicked:  # AI's turn if in AI mode
                turn_label.config(text=f"AI is thinking...")
                root.after(800, ai_move)  # Small delay for better UX
        else:
            button["text"] = player2_symbol
            button.config(fg=theme["o_color"])
            clicked = True
            count += 1
            update_turn_label()
            checkifwon()
    else:
        messagebox.showerror("Tic Tac Toe", "This box has already been selected!")

# Update the turn label
def update_turn_label():
    current_player = player1_name if clicked else player2_name
    symbol = player1_symbol if clicked else player2_symbol
    color = theme["x_color"] if clicked else theme["o_color"]
    turn_label.config(text=f"Turn: {current_player} ({symbol})")
    
    # Update status bar
    status_bar.config(text=f"Game in progress • {count} moves played")

# Reset the game
def reset():
    global buttons, clicked, count
    clicked = True
    count = 0
    for button in buttons:
        button.config(text=" ", bg=theme["button_bg"], fg=theme["button_fg"], state=NORMAL)
    update_turn_label()
    status_bar.config(text="New game started")
    
    # Hide tie restart button if visible
    if tie_button_frame.winfo_ismapped():
        tie_button_frame.pack_forget()
        for widget in tie_button_frame.winfo_children():
            widget.destroy()

# Exit the application
def exit_app():
    if messagebox.askyesno("Exit Game", "Are you sure you want to exit?"):
        root.quit()

# Navigate to the start screen
def go_to_start_screen():
    for widget in root.winfo_children():
        widget.destroy()
    create_start_screen_ui()

# Toggle theme
def toggle_theme():
    global current_theme, theme
    current_theme = "dark" if current_theme == "light" else "light"
    theme = themes[current_theme]
    
    # Update root background
    root.configure(bg=theme["bg"])
    
    # Recreate current screen
    current_screen = root.winfo_children()[0].winfo_name()
    for widget in root.winfo_children():
        widget.destroy()
        
    if current_screen == "start_frame":
        create_start_screen_ui()
    elif current_screen == "name_input_frame":
        create_name_input_ui()
    elif current_screen == "difficulty_frame":
        go_to_difficulty_selection()
    elif current_screen == "game_frame":
        create_game_ui()

# Navigate to the game screen
def start_game(difficulty=None):
    global ai_difficulty
    if difficulty:
        ai_difficulty = difficulty
    for widget in root.winfo_children():
        widget.destroy()
    create_game_ui()

# Navigate to the difficulty selection screen
def go_to_difficulty_selection():
    for widget in root.winfo_children():
        widget.destroy()
    
    main_frame = Frame(root, bg=theme["bg"], name="difficulty_frame")
    main_frame.pack(fill=BOTH, expand=TRUE, padx=20, pady=20)
    
    # Header
    ttk.Label(main_frame, text="Choose Difficulty", style="Title.TLabel", background=theme["bg"]).pack(pady=20)
    
    # Difficulty buttons with descriptions
    difficulties = [
        ("Easy", "Random moves by AI", "easy"),
        ("Medium", "AI tries to win or block you", "medium"),
        ("Hard", "AI uses minimax algorithm", "hard")
    ]
    
    for title, desc, diff in difficulties:
        diff_frame = Frame(main_frame, bg=theme["frame_bg"], padx=15, pady=10)
        diff_frame.pack(fill=X, pady=10)
        
        ttk.Label(diff_frame, text=title, style="Header.TLabel", background=theme["frame_bg"]).pack(anchor=W)
        ttk.Label(diff_frame, text=desc, background=theme["frame_bg"]).pack(anchor=W, pady=5)
        
        btn = ttk.Button(diff_frame, text="Select", command=lambda d=diff: start_game(d))
        btn.pack(anchor=E)
    
    # Back button
    ttk.Button(main_frame, text="Back", command=lambda: go_to_name_input(mode)).pack(pady=20)
    
    # Theme toggle button
    ttk.Button(main_frame, text=f"Switch to {'Dark' if current_theme == 'light' else 'Light'} Theme", 
               command=toggle_theme).pack(side=BOTTOM, pady=10)

# Navigate to the name input screen
def go_to_name_input(selected_mode):
    global mode
    mode = selected_mode
    for widget in root.winfo_children():
        widget.destroy()
    create_name_input_ui()

# Create the start screen UI
def create_start_screen_ui():
    main_frame = Frame(root, bg=theme["bg"], name="start_frame")
    main_frame.pack(fill=BOTH, expand=TRUE)
    
    # Title
    title_frame = Frame(main_frame, bg=theme["bg"], pady=40)
    title_frame.pack(fill=X)
    
    ttk.Label(title_frame, text="Tic Tac Toe", style="Title.TLabel", background=theme["bg"]).pack()
    ttk.Label(title_frame, text="A classic game of X and O", background=theme["bg"]).pack(pady=10)
    
    # Buttons frame
    button_frame = Frame(main_frame, bg=theme["bg"], pady=20)
    button_frame.pack()
    
    # Play buttons
    play_frame = Frame(button_frame, bg=theme["frame_bg"], padx=30, pady=20)
    play_frame.pack(fill=X, padx=50, pady=10)
    
    ttk.Label(play_frame, text="Select Game Mode", style="Header.TLabel", background=theme["frame_bg"]).pack(pady=10)
    
    btn_friend = Button(play_frame, text="Play with Friends", font=("Arial", 14), 
                        bg=theme["button_bg"], fg=theme["button_fg"], 
                        activebackground=theme["button_active_bg"],
                        padx=20, pady=10, bd=0,
                        command=lambda: go_to_name_input("friend"))
    btn_friend.pack(fill=X, pady=5)
    
    btn_ai = Button(play_frame, text="Play with AI", font=("Arial", 14), 
                    bg=theme["button_bg"], fg=theme["button_fg"], 
                    activebackground=theme["button_active_bg"],
                    padx=20, pady=10, bd=0,
                    command=lambda: go_to_name_input("ai"))
    btn_ai.pack(fill=X, pady=5)
    
    # Exit button
    btn_exit = Button(button_frame, text="Exit Game", font=("Arial", 12), 
                      bg=theme["button_bg"], fg=theme["button_fg"], 
                      activebackground=theme["button_active_bg"],
                      padx=15, pady=8, bd=0,
                      command=exit_app)
    btn_exit.pack(pady=20)
    
    # Theme toggle button
    ttk.Button(main_frame, text=f"{'🌙 ' if current_theme == '☀️' else '☀️🌙 '} ", 
               command=toggle_theme).pack(side=BOTTOM, pady=20)

# Create the name input screen UI
def create_name_input_ui():
    main_frame = Frame(root, bg=theme["bg"], name="name_input_frame")
    main_frame.pack(fill=BOTH, expand=TRUE, padx=20, pady=20)
    
    ttk.Label(main_frame, text="Player Information", style="Title.TLabel", background=theme["bg"]).pack(pady=20)
    
    # Input frame
    input_frame = Frame(main_frame, bg=theme["frame_bg"], padx=30, pady=30)
    input_frame.pack(fill=X)
    
    # Player 1 input
    p1_frame = Frame(input_frame, bg=theme["frame_bg"], pady=10)
    p1_frame.pack(fill=X)
    
    ttk.Label(p1_frame, text=f"Player 1 ({player1_symbol})", background=theme["frame_bg"]).pack(anchor=W)
    p1_entry = Entry(p1_frame, font=("Arial", 14), bd=0, highlightthickness=1, 
                    highlightbackground=theme["highlight_bg"], highlightcolor=theme["highlight_bg"])
    p1_entry.pack(fill=X, pady=5)
    p1_entry.insert(0, player1_name)
    
    # Player 2 input (only for friend mode)
    p2_entry = None
    if mode == "friend":
        p2_frame = Frame(input_frame, bg=theme["frame_bg"], pady=10)
        p2_frame.pack(fill=X)
        
        ttk.Label(p2_frame, text=f"Player 2 ({player2_symbol})", background=theme["frame_bg"]).pack(anchor=W)
        p2_entry = Entry(p2_frame, font=("Arial", 14), bd=0, highlightthickness=1, 
                        highlightbackground=theme["highlight_bg"], highlightcolor=theme["highlight_bg"])
        p2_entry.pack(fill=X, pady=5)
        p2_entry.insert(0, player2_name)
    
    # Button frame
    button_frame = Frame(main_frame, bg=theme["bg"], pady=20)
    button_frame.pack(fill=X)
    
    def submit_names():
        global player1_name, player2_name
        player1_name = p1_entry.get() or "Player 1"
        if mode == "friend" and p2_entry:
            player2_name = p2_entry.get() or "Player 2"
            start_game()  # For friend mode, start the game directly
        else:
            player2_name = "AI"
            go_to_difficulty_selection()  # For AI mode, go to difficulty selection
    
    btn_submit = Button(button_frame, text="Continue", font=("Arial", 14), 
                        bg=theme["button_bg"], fg=theme["button_fg"], 
                        activebackground=theme["button_active_bg"],
                        padx=20, pady=10, bd=0,
                        command=submit_names)
    btn_submit.pack(fill=X)
    
    # Back button
    ttk.Button(main_frame, text="Back to Main Menu", command=go_to_start_screen).pack(pady=10)
    
    # Theme toggle button
    ttk.Button(main_frame, text=f"Switch to {'Dark' if current_theme == 'light' else 'Light'} Theme", 
               command=toggle_theme).pack(side=BOTTOM, pady=10)

def create_game_ui():
    global buttons, turn_label, status_bar, tie_button_frame
    
    main_frame = Frame(root, bg=theme["bg"], name="game_frame")
    main_frame.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)
    
    # Game header - shows who's playing
    header_frame = Frame(main_frame, bg=theme["bg"], pady=10)
    header_frame.pack(fill=X)
    
    game_title = ttk.Label(header_frame, text="Tic Tac Toe", style="Header.TLabel", background=theme["bg"])
    game_title.pack()
    
    if mode == "ai":
        ttk.Label(header_frame, text=f"{player1_name} vs AI ({ai_difficulty.capitalize()})", 
                  background=theme["bg"]).pack()
    else:
        ttk.Label(header_frame, text=f"{player1_name} vs {player2_name}", background=theme["bg"]).pack()
    
    # Turn indicator
    turn_frame = Frame(main_frame, bg=theme["highlight_bg"], padx=10, pady=10)
    turn_frame.pack(fill=X, padx=20, pady=10)
    
    turn_label = ttk.Label(turn_frame, text=f"Turn: {player1_name} ({player1_symbol})", 
                          style="Status.TLabel", background=theme["highlight_bg"])
    turn_label.pack()
    
    # Main container with controls and game board
    content_container = Frame(main_frame, bg=theme["bg"])
    content_container.pack(fill=BOTH, expand=TRUE, pady=10)
    
    # Left panel for all controls
    control_panel = Frame(content_container, bg=theme["frame_bg"], width=300, padx=20, pady=20)
    control_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
    control_panel.pack_propagate(False)  # Fix the width
    
    # Control panel title
    ttk.Label(control_panel, text="Game Controls", background=theme["frame_bg"], 
             style="Header.TLabel").pack(pady=(0, 15))
    
    # Group all buttons in the control panel
    btn_restart = Button(control_panel, text="New Game", font=("Arial", 11), 
                        bg=theme["button_bg"], fg=theme["button_fg"], 
                        activebackground=theme["button_active_bg"],
                        padx=10, pady=5, bd=0,
                        command=reset)
    btn_restart.pack(fill=X, pady=5)
    
    btn_theme = Button(control_panel, text="🌙 ☀️", font=("Arial", 11), 
                      bg=theme["button_bg"], fg=theme["button_fg"], 
                      activebackground=theme["button_active_bg"],
                      padx=10, pady=5, bd=0,
                      command=toggle_theme)
    btn_theme.pack(fill=X, pady=5)
    
    btn_back = Button(control_panel, text="Back to Menu", font=("Arial", 11), 
                     bg=theme["button_bg"], fg=theme["button_fg"], 
                     activebackground=theme["button_active_bg"],
                     padx=10, pady=5, bd=0,
                     command=go_to_start_screen)
    btn_back.pack(fill=X, pady=5)
    
    btn_exit = Button(control_panel, text="Exit Game", font=("Arial", 11), 
                     bg=theme["button_bg"], fg=theme["button_fg"], 
                     activebackground=theme["button_active_bg"],
                     padx=10, pady=5, bd=0,
                     command=exit_app)
    btn_exit.pack(fill=X, pady=5)
    
    # Add some space
    Frame(control_panel, height=20, bg=theme["frame_bg"]).pack(fill=X)
    
    # Game stats section in control panel
    ttk.Label(control_panel, text="Game Info", background=theme["frame_bg"], 
             style="Header.TLabel").pack(pady=(10, 5))
    
    game_info = f"Mode: {'AI' if mode == 'ai' else 'Two Players'}"
    if mode == "ai":
        game_info += f"\nDifficulty: {ai_difficulty.capitalize()}"
    
    ttk.Label(control_panel, text=game_info, background=theme["frame_bg"]).pack(anchor=W)
    
    # Create custom font for buttons
    button_font = Font(family="Arial", size=24, weight="bold")
    
    # Game board container with a frame to center it
    game_container = Frame(content_container, bg=theme["bg"])
    game_container.pack(side=LEFT, fill=BOTH, expand=TRUE)
    
    # Center the game board
    game_frame = Frame(game_container, bg=theme["bg"], padx=10, pady=10)
    game_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Game buttons
    buttons = []
    for idx in range(9):
        row, col = idx // 3, idx % 3
        button = Button(game_frame, text=" ", font=button_font, 
                      height=2, width=4, bd=2, relief=RIDGE,
                      bg=theme["button_bg"], fg=theme["button_fg"],
                      activebackground=theme["button_active_bg"],
                      disabledforeground=theme["button_fg"],
                      command=lambda b=idx: b_click(b))
        button.grid(row=row, column=col, padx=5, pady=5)
        buttons.append(button)
    
    # Frame for tie restart button (initially hidden)
    tie_button_frame = Frame(main_frame, bg=theme["highlight_bg"], padx=10, pady=5)
    
    # Status bar
    status_frame = Frame(main_frame, bg=theme["frame_bg"], pady=5)
    status_frame.pack(fill=X, side=BOTTOM)
    
    status_bar = ttk.Label(status_frame, text="New game started", background=theme["frame_bg"])
    status_bar.pack(side=LEFT, padx=10)

# Initialize the start screen
create_start_screen_ui()
root.mainloop()