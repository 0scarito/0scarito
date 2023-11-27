import tkinter as tk
import random

# Create the main window
window = tk.Tk()
window.title("Memory Puzzle Game")

# Difficulty levels and settings
difficulty_levels = {
    'Easy': {'grid_size': 4, 'time_limit': 90},
    'Medium': {'grid_size': 8, 'time_limit': 60},
    'Hard': {'grid_size': 16, 'time_limit': 30}
}

# Initialize global variables
buttons = []
selected = []
timer_initial = 60
timer_label = None
current_difficulty = 'Easy'  # Default difficulty
base_score = 1000  # Starting score
move_count = 0  # Number of moves made
score_label = None  # Label to display the score

# Function to generate images
def generate_images(grid_size):
    basic_images = ["🍎", "🍌", "🍇", "🍒", "🍓", "🍉", "🍍", "🥥"]
    images = basic_images[:grid_size // 2] * 2
    random.shuffle(images)
    return images

# Function to update the timer
def update_timer():
    global timer_initial
    if timer_initial > 0:
        timer_initial -= 1
        timer_label.config(text=f"Time left: {timer_initial}s")
        window.after(1000, update_timer)
    else:
        for btn in buttons:
            btn.config(state='disabled')
        check_game_over()  # Check if game is over to finalize score

# Function to reveal a card
def reveal_card(index):
    global move_count, base_score
    if len(selected) < 2:
        buttons[index].config(text=images[index])
        selected.append(index)
        if len(selected) == 2:
            move_count += 1
            base_score -= 10  # Decrease score for each move
            score_label.config(text=f"Score: {base_score}")
            window.after(1000, check_match)

# Function to check for a match
def check_match():
    idx1, idx2 = selected
    if images[idx1] == images[idx2]:
        buttons[idx1].config(state="disabled")
        buttons[idx2].config(state="disabled")
        check_game_over()  # Check if game is over to finalize score
    else:
        buttons[idx1].config(text=" ")
        buttons[idx2].config(text=" ")
    selected.clear()

# Function to check if the game is over and update the score
def check_game_over():
    if all(button['state'] == 'disabled' for button in buttons):
        global base_score, timer_initial
        time_bonus = timer_initial * 5  # Example bonus calculation
        base_score += time_bonus
        score_label.config(text=f"Final Score: {base_score}")

# Function to initialize the game based on difficulty
def initialize_game(difficulty):
    global timer_initial, buttons, images, move_count, base_score

    current_difficulty = difficulty
    timer_initial = difficulty_levels[difficulty]['time_limit']
    grid_size = difficulty_levels[difficulty]['grid_size']
    images = generate_images(grid_size)

    # Clear existing buttons and reset score
    for btn in buttons:
        btn.destroy()
    buttons.clear()
    selected.clear()
    move_count = 0
    base_score = 1000
    score_label.config(text=f"Score: {base_score}")

    # Create new grid of buttons
    for i in range(grid_size):
        button = tk.Button(window, text=" ", width=10, height=5,
                           command=lambda i=i: reveal_card(i))
        button.grid(row=1 + i // (grid_size // 4), column=i % (grid_size // 4))
        buttons.append(button)

    timer_label.config(text=f"Time left: {timer_initial}s")
    update_timer()

# Create labels for timer and score
timer_label = tk.Label(window, text=f"Time left: {timer_initial}s")
timer_label.grid(row=0, column=0, columnspan=4)
score_label = tk.Label(window, text=f"Score: {base_score}")
score_label.grid(row=2, column=0, columnspan=4)

# Difficulty selection menu
difficulty_menu = tk.Menu(window)
window.config(menu=difficulty_menu)

def set_difficulty(level):
    initialize_game(level)

diff_submenu = tk.Menu(difficulty_menu, tearoff=0)
difficulty_menu.add_cascade(label="Difficulty", menu=diff_submenu)
for level in difficulty_levels:
    diff_submenu.add_command(label=level, command=lambda level=level: set_difficulty(level))

initialize_game(current_difficulty)

window.mainloop()
