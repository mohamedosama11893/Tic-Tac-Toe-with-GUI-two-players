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