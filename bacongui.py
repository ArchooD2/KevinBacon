import tkinter as tk
import threading
from baconwaffle import find_shortest_path

def search_path():
    start = source_entry.get()
    end = target_entry.get()
    depth = int(depth_entry.get())
    result_text.delete(1.0, tk.END)  # Clear previous results
    
    # Run find_shortest_path in a separate thread
    threading.Thread(target=run_search_path, args=(start, end, depth)).start()

def run_search_path(start, end, depth):
    result = find_shortest_path(start, end, depth)
    if result:
        root.after(0, lambda: display_result(f"Found path:\n" + "\n".join(result)))
    else:
        root.after(0, lambda: display_result("No path found."))

def display_result(text):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)

# Create the main window
root = tk.Tk()
root.title("BaconWaffle Wikipedia Path Finder")

# GUI elements
source_label = tk.Label(root, text="Source Article:")
source_label.grid(row=0, column=0)
source_entry = tk.Entry(root)
source_entry.grid(row=0, column=1)

target_label = tk.Label(root, text="Target Article:")
target_label.grid(row=1, column=0)
target_entry = tk.Entry(root)
target_entry.grid(row=1, column=1)

depth_label = tk.Label(root, text="Maximum Depth:")
depth_label.grid(row=2, column=0)
depth_entry = tk.Entry(root)
depth_entry.grid(row=2, column=1)

search_button = tk.Button(root, text="Search", command=search_path)
search_button.grid(row=3, column=0)

clear_button = tk.Button(root, text="Clear", command=lambda: result_text.delete(1.0, tk.END))
clear_button.grid(row=3, column=1)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=4, columnspan=2)

# Start the GUI main loop
root.mainloop()
