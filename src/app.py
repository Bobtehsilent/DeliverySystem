import os
import sys
import time
import datetime
import random
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from src.optimizer import Optimizer
from src.data_processing import load_data, validate_data, save_results
from src.visualization import visualize_logs, visualize_histogram, visualize_fitness

base_dir = os.path.abspath("..")  
sys.path.append(base_dir) 

DATA_DIR = os.path.join(base_dir, "data", 'to_process')
RESULTS_DIR = os.path.join(base_dir, "results")
EXPECTED_HEADERS = ["Paket_id", "Vikt", "Förtjänst", "Deadline"]

def check_file(file_path):
    """Kontrollera om filen är en CSV och har rätt format."""
    if not file_path.endswith(".csv"):
        print(f"Invalid file format: {file_path}. Expected a .csv file.")
        return False

    try:
        df = pd.read_csv(file_path, nrows=1)  # Läs endast första raden
        if list(df.columns) != EXPECTED_HEADERS:
            print(f"Invalid file headers: {file_path}. Expected {EXPECTED_HEADERS}.")
            return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False
    print(f"File {file_path} is valid.")
    return True

def process_files():
    """Process all files in data/to_process."""
    for file_name in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.isfile(file_path):
            continue
        if not check_file(file_path):
            print(f"Skipping invalid file: {file_name}")
            continue

        # Display a log window during processing
        log_window = create_log_window()
        run_id = random.randint(1, 9999)  # Unique ID for this run

        packages = load_data(file_path)
        valid, message = validate_data(packages)
        if not valid:
            log_window.append_log(f"Validation failed for {file_name}: {message}")
            log_window.destroy()
            continue

        optimizer = Optimizer(packages, log_file=os.path.join(base_dir, "logs", f"optimization_{run_id}.log"))
        stats, best_solution = optimizer.optimize(population_size=100, generations=200, patience=5)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_dir = os.path.join(RESULTS_DIR, f"{timestamp}_run")

        result_file, truck_details_file = save_results(optimizer, result_dir, timestamp)

        visualize_fitness(stats)
        optimizer.analyze_solution()

        # Close log window
        log_window.append_log("Optimization completed.")
        log_window.destroy()

        # Display the saved files in a new window
        display_results_window(result_file, truck_details_file)


def schedule_run():
    """Schemalägg körning klockan 05:00"""
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=5, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time = target_time + datetime.timedelta(days=1)

        time_until_run = (target_time - now).total_seconds()
        print(f"Next run scheduled in {time_until_run} seconds")
        time.sleep(time_until_run)
        process_files()

def run_now(file_path=None):
    """Run optimization immediately."""
    if file_path is None:
        file_path = filedialog.askopenfilename(initialdir="data", title="Select a File")
    if not file_path or not os.path.isfile(file_path):
        print("No file selected or file not found.")
        return
    if not check_file(file_path):
        print("Selected file is not valid.")
        return

    # Disable main GUI during run
    root = tk.Tk()
    root.withdraw()  # Hide the main window temporarily

    log_window = create_log_window()
    run_id = random.randint(1, 9999)

    try:
        packages = load_data(file_path)
        valid, message = validate_data(packages)
        if not valid:
            log_window.append_log(f"Validation failed: {message}")
            return

        optimizer = Optimizer(packages, log_file=os.path.join(base_dir, "logs", f"optimization_{run_id}.log"))
        stats, best_solution = optimizer.optimize(population_size=100, generations=200, patience=5)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_dir = os.path.join(RESULTS_DIR, f"{timestamp}_run")

        result_file, truck_details_file = save_results(optimizer, result_dir, timestamp)

        visualize_fitness(stats)
        optimizer.analyze_solution()

        # Display the saved files in a new window
        display_results_window(result_file, truck_details_file)
    finally:
        log_window.append_log("Optimization completed.")
        log_window.destroy()
        root.deiconify()  # Restore main GUI

def create_log_window():
    """Create a new window to display live logs."""
    class LogWindow:
        def __init__(self):
            self.window = tk.Toplevel()
            self.window.title("Optimization Progress")
            self.window.geometry("600x400")
            self.text_area = tk.Text(self.window, wrap=tk.WORD, font=("Helvetica", 10))
            self.text_area.pack(expand=1, fill=tk.BOTH)
            self.text_area.insert(tk.END, "Starting optimization...\n")
            self.text_area.config(state=tk.DISABLED)

        def append_log(self, message):
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, message + "\n")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)

        def destroy(self):
            self.window.destroy()

    return LogWindow()

def display_results_window(result_file, truck_details_file):
    """Open a new window to display the saved results."""
    def read_file_content(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    result_window = tk.Toplevel()
    result_window.title("Optimization Results")
    result_window.geometry("600x400")

    text_area = tk.Text(result_window, wrap=tk.WORD, font=("Helvetica", 10))
    text_area.pack(expand=1, fill=tk.BOTH)

    result_content = (
        f"--- Results ---\n\n{read_file_content(result_file)}\n\n"
        f"--- Truck Details ---\n\n{read_file_content(truck_details_file)}"
    )
    text_area.insert(tk.END, result_content)

    text_area.config(state=tk.DISABLED)


def create_gui():
    """Skapa en enkel GUI-app."""
    root = tk.Tk()
    root.title("Delivery optimization App")
    root.geometry("800x400")

    tk.Label(root, text="Optimizer Control", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Run Now", command=lambda: run_now(None)).pack(pady=5)
    tk.Button(root, text="Select and Run", command=lambda: run_now()).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    # Countdown to 05:00
    def update_timer():
        now = datetime.datetime.now()
        target_time = now.replace(hour=5, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += datetime.timedelta(days=1)

        time_left = target_time - now
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"Next run in: {hours:02}:{minutes:02}:{seconds:02}")
        root.after(1000, update_timer)

    timer_label = tk.Label(root, text="", font=("Helvetica", 12))
    timer_label.pack(pady=10)
    update_timer()

    root.mainloop()

if __name__ == "__main__":
    create_gui()