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
