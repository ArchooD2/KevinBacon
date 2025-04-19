import tkinter as tk
import threading
from tkinter import ttk
import logging
from baconwaffle import find_shortest_path

DEFAULT_DEPTH = 7

# --- Logging Setup ---
logger = logging.getLogger("BaconWaffleGUI")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Custom handler for Tkinter Text widget
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        # Ensure thread-safe GUI update
        self.text_widget.after(0, self.append, log_entry)

    def append(self, log_entry):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, log_entry + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

def search_path():
    start = source_entry.get()
    end = target_entry.get()
    try:
        depth = int(depth_entry.get()) if depth_entry.get() else DEFAULT_DEPTH
    except ValueError:
        depth = DEFAULT_DEPTH
        logger.warning("Invalid depth input. Using default depth %d.", DEFAULT_DEPTH)
    result_text.delete(1.0, tk.END)
    search_button.config(state='disabled')
    logger.info("Starting search: '%s' -> '%s' (max depth %d)", start, end, depth)
    threading.Thread(target=run_search_path, args=(start, end, depth)).start()

def run_search_path(start, end, depth):
    try:
        result = find_shortest_path(start, end, depth)
        root.after(0, lambda: display_result(result))
        if result:
            logger.info("Path found: %s", " -> ".join(result))
        else:
            logger.info("No path found between '%s' and '%s'.", start, end)
    except Exception as e:
        logger.error("Error during search: %s", e)
        root.after(0, lambda: display_result(None))

def display_result(result):
    search_button.config(state='normal')
    result_text.delete(1.0, tk.END)
    if result:
        result_text.insert(tk.END, "Found path:\n" + "\n".join(result))
    else:
        result_text.insert(tk.END, "No path found.")

# --- GUI Setup ---
root = tk.Tk()
root.title("BaconWaffle Wikipedia Path Finder")
root.geometry("600x550")
root.resizable(False, False)

style = ttk.Style()
style.configure('TLabel', font=('Arial', 10), padding=5)
style.configure('TButton', font=('Arial', 10), padding=5)
style.configure('TEntry', font=('Arial', 10), padding=5)

input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill='x')

ttk.Label(input_frame, text="Source Article:").grid(row=0, column=0, sticky='w')
source_entry = ttk.Entry(input_frame, width=40)
source_entry.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(input_frame, text="Target Article:").grid(row=1, column=0, sticky='w')
target_entry = ttk.Entry(input_frame, width=40)
target_entry.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(input_frame, text="Maximum Depth:").grid(row=2, column=0, sticky='w')
depth_entry = ttk.Entry(input_frame, width=10)
depth_entry.grid(row=2, column=1, sticky='w', padx=5, pady=2)
depth_entry.insert(0, str(DEFAULT_DEPTH))

button_frame = ttk.Frame(root, padding=10)
button_frame.pack(fill='x')

search_button = ttk.Button(button_frame, text="Search", command=search_path)
search_button.pack(side='left', padx=5)

clear_button = ttk.Button(
    button_frame,
    text="Clear",
    command=lambda: result_text.delete(1.0, tk.END)
)
clear_button.pack(side='left', padx=5)

result_frame = ttk.Frame(root, padding=10)
result_frame.pack(fill='both', expand=True)

result_text = tk.Text(
    result_frame,
    height=10,
    width=70,
    font=('Arial', 10),
    wrap=tk.WORD,
)
result_scroll = ttk.Scrollbar(result_frame, command=result_text.yview)
result_text.configure(yscrollcommand=result_scroll.set)

result_text.grid(row=0, column=0, sticky='nsew')
result_scroll.grid(row=0, column=1, sticky='ns')
result_frame.grid_columnconfigure(0, weight=1)
result_frame.grid_rowconfigure(0, weight=1)

# --- Logging Text Area ---
log_label = ttk.Label(root, text="Log:")
log_label.pack(anchor='w', padx=15)

log_frame = ttk.Frame(root, padding=(10,0,10,10))
log_frame.pack(fill='both', expand=True)

log_text = tk.Text(
    log_frame,
    height=10,
    width=70,
    font=('Consolas', 9),
    wrap=tk.WORD,
    state='disabled',
    bg='white',
    foreground='black'
)
log_scroll = ttk.Scrollbar(log_frame, command=log_text.yview)
log_text.configure(yscrollcommand=log_scroll.set)


log_text.grid(row=0, column=0, sticky='nsew')
log_scroll.grid(row=0, column=1, sticky='ns')
log_frame.grid_columnconfigure(0, weight=1)
log_frame.grid_rowconfigure(0, weight=1)

# Add the custom text handler to logger
text_handler = TextHandler(log_text)
text_handler.setFormatter(formatter)
logger.addHandler(text_handler)

logger.info("Application started.")

root.mainloop()
