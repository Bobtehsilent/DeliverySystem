import os
import sys
import time
import datetime
import random
import threading
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from src.optimizer import Optimizer
from src.data_processing import load_data, validate_data, save_results
from src.visualization import visualize_histogram, visualize_fitness, leftover_histogram

base_dir = os.path.abspath(".")  
sys.path.append(base_dir) 

DATA_DIR = os.path.join(base_dir, "data", 'to_process')
RESULTS_DIR = os.path.join(base_dir, "results")
EXPECTED_HEADERS = ["Paket_id", "Vikt", "Förtjänst", "Deadline"]
generations = 200
population_size = 100

def check_file(file_path):
    """Kontrollera om filen är en CSV och har rätt format."""
    if not file_path.endswith(".csv"):
        print(f"Invalid file format: {file_path}. Expected a .csv file.")
        return False

    try:
        df = pd.read_csv(file_path, nrows=1)  
        if list(df.columns) != EXPECTED_HEADERS:
            print(f"Invalid file headers: {file_path}. Expected {EXPECTED_HEADERS}.")
            return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False
    print(f"File {file_path} is valid.")
    return True

def process_files(file_path=None):
    """Behandlar vald fil från run_now eller från scheduled_run. Kör optimering och sparar resultat."""
    files_to_process = []

    if file_path:
        files_to_process.append(file_path)
    else:
        files_to_process = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]

    for file_path in files_to_process:
        if not check_file(file_path):
            print(f"Skipping invalid file: {file_path}")
            continue

        run_id = random.randint(1, 9999)
        result_dir = os.path.join(RESULTS_DIR, f"run_{run_id}")
        os.makedirs(result_dir, exist_ok=True)
        log_file = os.path.join(base_dir, "logs", f"optimization_{run_id}.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        log_window = create_log_window()

        def optimization_task():
            try:
                packages = load_data(file_path)
                valid, message = validate_data(packages)
                if not valid:
                    log_window.append_log(f"Validation failed: {message}")
                    return

                optimizer = Optimizer(packages, log_file=log_file)
                stats, best_solution = optimizer.optimize(
                    population_size=population_size, generations=generations, patience=5, run_id=run_id, log_window=log_window
                )

                result_file, truck_details_file = save_results(optimizer, result_dir, f"run_{run_id}")

                def save_visualizations():
                    visualize_fitness(stats, result_dir)
                    truck_weights = [truck.get_total_weight() for truck in optimizer.trucks]
                    truck_profits = [truck.get_total_profit() for truck in optimizer.trucks]
                    visualize_histogram(truck_weights, truck_profits, result_dir)
                    leftover_histogram(optimizer.trucks, optimizer.packages, result_dir)

                log_window.window.after(0, save_visualizations)

                final_log_file = os.path.join(result_dir, f"run_{run_id}.log")
                try:
                    os.rename(log_file, final_log_file)
                    log_window.append_log(f"Log file moved to: {final_log_file}")
                except Exception as e:
                    log_window.append_log(f"Failed to move log file: {e}")
                    return

                log_window.append_log(f"Optimization completed for run_id {run_id}.")
                log_window.window.after(
                    0, lambda: display_results_window(result_file, truck_details_file, result_dir)
                )
            except Exception as e:
                log_window.append_log(f"Error: {e}")
            finally:
                if os.path.exists(log_file):
                    try:
                        os.remove(log_file)
                        log_window.append_log(f"Original log file deleted: {log_file}")
                    except Exception as e:
                        log_window.append_log(f"Failed to delete original log file: {e}")

                log_window.append_log("Closing log window...")
                log_window.window.after(0, log_window.destroy)

        threading.Thread(target=optimization_task).start()

def schedule_run():
    """En schemalagd körning som ska köras varje dag vid 05:00"""
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=5, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += datetime.timedelta(days=1)

        time_until_run = (target_time - now).total_seconds()
        print(f"Next run scheduled in {time_until_run:.2f} seconds.")
        time.sleep(time_until_run)

        files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
        if not files:
            print("No files available in the data directory.")
            continue

        file_to_process = files[0]  
        print(f"Scheduled run started for: {file_to_process}")
        process_files(file_to_process)

def run_now():
    """Kör optimering direkt för vald fil eller första fil i to_process mappen."""
    files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]

    if files:
        file_to_process = files[0]
        print(f"Processing file from to_process: {file_to_process}")
        process_files(file_to_process)
    else:
        file_path = filedialog.askopenfilename(initialdir=os.path.join(base_dir, 'data'), title="Select a File")
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "No valid file selected.")
            return

        print(f"Processing selected file: {file_path}")
        process_files(file_path)

def create_log_window(total_generations=generations):
    """Skapar ett separat fönster för att visa loggning och framsteg."""
    class LogWindow:
        def __init__(self):
            self.window = tk.Toplevel()
            self.window.title("Delivery Optimization")
            self.window.geometry("600x500")

            self.text_area = tk.Text(self.window, wrap=tk.WORD, font=("Helvetica", 10))
            self.text_area.pack(expand=1, fill=tk.BOTH)

            self.progress_label = tk.Label(self.window, text="Progress: 0%", font=("Helvetica", 12))
            self.progress_label.pack(pady=5)
            self.progress_bar = tk.Canvas(self.window, width=400, height=20, bg="white")
            self.progress_bar.pack(pady=5)

            self.total_generations = total_generations
            self.current_generation = 0
            self.progress_bar_fill = self.progress_bar.create_rectangle(0, 0, 0, 20, fill="green")

        def append_log(self, message):
            self.window.after(0, self._append_log, message)

        def _append_log(self, message):
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, message)
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)

        def update_progress(self, generation):
            self.current_generation = generation
            percentage = (generation / self.total_generations) * 100
            self.progress_label.config(text=f"Progress: {percentage:.1f}%")
            self.progress_bar.coords(self.progress_bar_fill, 0, 0, 4 * percentage, 20)

        def destroy(self):
            self.window.destroy()

    return LogWindow()

def display_results_window(result_file, truck_details_file, result_dir):
    """Öppnar separata fönster för att visa resultat och histogram."""
    def read_file_content(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    result_window = tk.Toplevel()
    result_window.title("Optimization Results")
    result_window.geometry("800x600+100+100") 

    text_area = tk.Text(result_window, wrap=tk.WORD, font=("Helvetica", 10))
    text_area.pack(expand=1, fill=tk.BOTH, side=tk.LEFT)

    result_content = (
        f"--- Results ---\n\n{read_file_content(result_file)}\n\n"
        f"--- Truck Details ---\n\n{read_file_content(truck_details_file)}"
    )
    text_area.insert(tk.END, result_content)
    text_area.config(state=tk.DISABLED)

    if result_dir:
        truck_dist_path = os.path.join(result_dir, "truck_distribution.png")
        fitness_evolution_path = os.path.join(result_dir, "fitness_evolution.png")
        leftover_dist_path = os.path.join(result_dir, "leftover_distribution.png")

        if os.path.exists(truck_dist_path):
            create_histogram_window(truck_dist_path, "Truck Distribution", x_offset=920, y_offset=100)

        if os.path.exists(fitness_evolution_path):
            create_histogram_window(fitness_evolution_path, "Fitness Evolution", x_offset=100, y_offset=550)

        if os.path.exists(leftover_dist_path):
            create_histogram_window(leftover_dist_path, "Leftover Distribution", x_offset=920, y_offset=550)

def create_histogram_window(image_path, title, x_offset=0, y_offset=0):
    """skapa ett dynamiskt histogram fönster för att visa bilder."""
    img_window = tk.Toplevel()
    img_window.title(title)

    width, height = 800, 600
    img_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    original_img = Image.open(image_path)

    canvas = tk.Canvas(img_window, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    def resize_image(event):
        new_width = event.width
        new_height = event.height

        resized_img = original_img.resize((new_width, new_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized_img)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=tk_img)
        canvas.image = tk_img 

    img_window.bind("<Configure>", resize_image)

def view_results():
    """Öppnar en lista av resultat filer för att visa detaljer."""
    result_folders = [folder for folder in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, folder))]

    if not result_folders:
        messagebox.showinfo("No Results", "No result folders available.")
        return

    result_window = tk.Toplevel()
    result_window.title("Available Results")
    result_window.geometry("800x400")

    tk.Label(result_window, text="Select a result folder to view:", font=("Helvetica", 12)).pack(pady=10)

    listbox = tk.Listbox(result_window, font=("Helvetica", 10))
    listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for folder in result_folders:
        listbox.insert(tk.END, folder)

    def open_selected_result():
        """Öppnar valda resultatfiler för visning."""
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a folder to view.")
            return

        folder_name = listbox.get(selected[0])
        result_dir = os.path.join(RESULTS_DIR, folder_name)

        result_file = os.path.join(result_dir, f"{folder_name}_results.txt")
        truck_details_file = os.path.join(result_dir, f"{folder_name}_truck_details.txt")

        if os.path.exists(result_file) and os.path.exists(truck_details_file):
            display_results_window(result_file, truck_details_file, result_dir)
        else:
            messagebox.showerror("Error", "Result files not found in the selected folder.")

    tk.Button(result_window, text="Open", command=open_selected_result).pack(pady=10)
    tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=5)

def create_gui():
    """Skapar main GUI för applikationen."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    root = tk.Tk()
    root.title("Delivery Optimization App")
    root.geometry("800x400")

    tk.Label(root, text="Optimizer Control", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Run Now", command=lambda: run_now()).pack(pady=5)

    tk.Button(root, text="View Results", command=view_results).pack(pady=5)

    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

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

    def start_schedule():
        threading.Thread(target=schedule_run, daemon=True).start()

    timer_label = tk.Label(root, text="", font=("Helvetica", 12))
    timer_label.pack(pady=10)
    update_timer()

    start_schedule()

    root.mainloop()

if __name__ == "__main__":
    create_gui()