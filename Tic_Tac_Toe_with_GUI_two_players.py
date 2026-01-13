import tkinter as tk
import random
import glob
from PIL import Image, ImageTk

# ================================================================
# WORKFLOW (high-level)
# 1) Start program -> create root Tk window.
# 2) Find X/O image files under assets/characters/ with glob.
# 3) Load and resize images using PIL then convert to PhotoImage.
# 4) Build top frame: score label, current-turn label, winner label, restart button.
# 5) Build bottom frame: a 3x3 grid of Buttons stored in cell_buttons.
# 6) Player clicks a cell -> next_turn(row, col):
#      - if the cell is empty and no winner: place current player's symbol (image + text)
#      - check for win or tie; update result and scores if needed
#      - switch player turn and update player label
# 7) The GUI runs inside window.mainloop().
# ================================================================

def load_game_assets(category):
    """
    Search for PNG images inside the assets/<category>/ folder and return a dict
    mapping "X" and "O" to file paths when possible (case-insensitive).
    """
    pattern = f"assets/{category}/*.png"
    files = glob.glob(pattern)
    assets = {}
    for file in files:
        if "x" in file.lower():
            assets["X"] = file
        elif "o" in file.lower():
            assets["O"] = file
    return assets

# ----------- Game functions -----------

def next_turn(row, col):
    """
    Handle a player clicking on (row, col).
    - If the chosen cell is empty and there is no winner, place the current player's symbol.
    - Then check for a winner or tie and update UI/state accordingly.
    - Finally switch the current player and update the player label.
    """
    global player
    if cell_buttons[row][col]['text'] == '' and not check_win():
        # place the current player's symbol (image + text)
        if player == 'X':
            cell_buttons[row][col].config(image=x_img, text='X')
        else:
            cell_buttons[row][col].config(image=o_img, text='O')

        # check for a winner
        winner = check_win()
        if winner:
            result_text.set(f"{winner} Wins!")
            # update scores
            if winner == 'X':
                user_score.set(user_score.get() + 1)
            else:
                computer_score.set(computer_score.get() + 1)
            score_text.set(f"You: {user_score.get()} Computer: {computer_score.get()}")
            return

        # check for tie (no empty spaces)
        if not check_empty_spaces():
            result_text.set("Tie!")
            for r in range(3):
                for c in range(3):
                    cell_buttons[r][c].config(bg='red')
            return

        # switch player and update label
        player = 'O' if player == 'X' else 'X'
        player_label.config(text=f"Player Turn: {player}")
        
def check_win():
    """
    Return 'X' or 'O' if a winning line is found; otherwise return False.
    Highlights winning cells by changing their background color.
    """
    # rows
    for r in range(3):
        if (cell_buttons[r][0]['text'] != '' and
                cell_buttons[r][0]['text'] == cell_buttons[r][1]['text'] == cell_buttons[r][2]['text']):
            cell_buttons[r][0].config(bg='cyan')
            cell_buttons[r][1].config(bg='cyan')
            cell_buttons[r][2].config(bg='cyan')
            return cell_buttons[r][0]['text']
    # columns
    for c in range(3):
        if (cell_buttons[0][c]['text'] != '' and
                cell_buttons[0][c]['text'] == cell_buttons[1][c]['text'] == cell_buttons[2][c]['text']):
            cell_buttons[0][c].config(bg='cyan')
            cell_buttons[1][c].config(bg='cyan')
            cell_buttons[2][c].config(bg='cyan')
            return cell_buttons[0][c]['text']
    # diagonals
    if (cell_buttons[0][0]['text'] != '' and
            cell_buttons[0][0]['text'] == cell_buttons[1][1]['text'] == cell_buttons[2][2]['text']):
        cell_buttons[0][0].config(bg='cyan')
        cell_buttons[1][1].config(bg='cyan')
        cell_buttons[2][2].config(bg='cyan')
        return cell_buttons[0][0]['text']
    if (cell_buttons[0][2]['text'] != '' and
            cell_buttons[0][2]['text'] == cell_buttons[1][1]['text'] == cell_buttons[2][0]['text']):
        cell_buttons[0][2].config(bg='cyan')
        cell_buttons[1][1].config(bg='cyan')
        cell_buttons[2][0].config(bg='cyan')
        return cell_buttons[0][2]['text']
    return False

def check_empty_spaces():
    """
    Return True if there is at least one empty cell, otherwise False.
    """
    for r in range(3):
        for c in range(3):
            if cell_buttons[r][c]['text'] == '':
                return True
    return False


def start_new_game():
    """
    Choose a random starting player, update the player label and recreate
    the 3x3 button grid (resetting each button).
    """
    global player
    player = random.choice(players)
    player_label.config(text=f"Player Turn: {player}")
    for r in range(3):
        for c in range(3):
            btn = tk.Button(bottom_frame, text="", font=("Arial", 50, "bold"), width=4, height=1,
                            command=lambda rr=r, cc=c: next_turn(rr, cc))
            cell_buttons[r][c] = btn
            btn.grid(row=r, column=c, sticky="nsew")

# ----------- GUI -----------

window = tk.Tk()
window.title("X O Game by Mohamed Osama")
# window.geometry("420x790")
window.resizable(False, False)

# load image assets
assets = load_game_assets("characters")

# resize and convert images using PIL then make PhotoImage for Tkinter
x_img = Image.open(assets["X"])
x_img = x_img.resize((100, 100))
x_img = ImageTk.PhotoImage(x_img)

o_img = Image.open(assets["O"])
o_img = o_img.resize((100, 100))
o_img = ImageTk.PhotoImage(o_img)

# important state variables
players = ["X", "O"]
player = random.choice(players)

user_score = tk.IntVar(value=0)
computer_score = tk.IntVar(value=0)
result_text = tk.StringVar(value="")
score_text = tk.StringVar(value=f"You: {user_score.get()} Computer: {computer_score.get()}")

# -------- Frame 1 (labels + restart) --------
top_frame = tk.Frame(window)
top_frame.pack(pady=20)

result_label = tk.Label(top_frame, textvariable=score_text, font=("Arial", 16, "bold"))
result_label.pack()

player_label = tk.Label(top_frame, text=f"Player Turn: {player}", font=("Arial", 20))
player_label.pack(pady=10)

winner_label = tk.Label(top_frame, textvariable=result_text, font=("Arial", 20))
winner_label.pack(pady=10)

restart_button = tk.Button(top_frame, text="restart", font=("Arial", 20), command=start_new_game)
restart_button.pack(pady=10)

# -------- Frame 2 (game board) --------
bottom_frame = tk.Frame(window)
bottom_frame.pack()

# buttons matrix (initialized as None placeholders)
cell_buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        btn = tk.Button(bottom_frame, text="", font=("Arial", 50, "bold"), width=4, height=1,
                        command=lambda r=row, c=col: next_turn(r, c))
        cell_buttons[row][col] = btn
        btn.grid(row=row, column=col, sticky="nsew")

# configure row/column weights and minimum sizes so buttons keep a good size
for i in range(3):
    bottom_frame.grid_rowconfigure(i, weight=1, minsize=150)
    bottom_frame.grid_columnconfigure(i, weight=1, minsize=200)

# -------- Main loop --------
window.mainloop()