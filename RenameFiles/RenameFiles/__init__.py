import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import datetime

'''
Author: Jacob J
Last Edit Date: 3/29/24

This GUI Program Appends file names, adding or deleting parts.
'''
class FileRenamerGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Renamer Tool")

        # Directory Path Entry
        self.path_label = tk.Label(master, text="Directory Path:")
        self.path_label.grid(row=0, column=0, sticky='e')

        self.path_entry = tk.Entry(master, width=50)
        self.path_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=2)

        # Rename Options and Entry Field for Text to Add or Remove
        self.rename_option_var = tk.StringVar()
        self.rename_option_var.set("append_start")
        self.append_start_radio = tk.Radiobutton(master, text="Append at Start", variable=self.rename_option_var,
                                                 value="append_start")
        self.append_start_radio.grid(row=1, column=0, columnspan=1)
        self.append_end_radio = tk.Radiobutton(master, text="Append at End", variable=self.rename_option_var,
                                               value="append_end")
        self.append_end_radio.grid(row=1, column=1, columnspan=1)
        self.remove_word_radio = tk.Radiobutton(master, text="Remove Word", variable=self.rename_option_var,
                                                value="remove_word")
        self.remove_word_radio.grid(row=1, column=2, columnspan=1)

        self.text_entry = tk.Entry(master, width=50)
        self.text_entry.grid(row=2, column=0, columnspan=3)

        # Start Button
        self.start_button = tk.Button(master, text="Start Renaming", command=self.start_renaming)
        self.start_button.grid(row=3, column=0, columnspan=3)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(master, width=70, height=10)
        self.log_area.grid(row=4, column=0, columnspan=3)
        self.log_area.config(state='disabled')

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def start_renaming(self):
        dir_path = self.path_entry.get()
        action = self.rename_option_var.get()
        text = self.text_entry.get()

        # Validate directory path
        if not dir_path or not os.path.isdir(dir_path):
            messagebox.showerror("Error", "Invalid directory path.")
            return

        # Validate text input for certain actions
        if action != 'remove_word' and not text:
            messagebox.showerror("Error", "Please enter text to add or remove.")
            return

        # Prepare the logs directory and log file
        log_dir = os.path.join(dir_path, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, datetime.datetime.now().strftime("renaming_log_%Y-%m-%d_%H-%M-%S.txt"))

        # Start logging
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"Renaming operation started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        try:
            files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
            for filename in files:
                # Skip the log file itself
                if filename.startswith("renaming_log_"):
                    continue

                new_name = filename
                if action == 'append_start':
                    new_name = f"{text}{filename}"
                elif action == 'append_end':
                    name, ext = os.path.splitext(filename)
                    new_name = f"{name}{text}{ext}"
                elif action == 'remove_word':
                    new_name = filename.replace(text, "")

                # Rename the file if there's a change
                if new_name != filename:
                    os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_name))
                    # Log each rename action
                    with open(log_file_path, 'a') as log_file:
                        log_file.write(f"Renamed {filename} to {new_name}\n")
                    self.log_message(f"Renamed {filename} to {new_name}")

            self.log_message("Renaming operation completed. Check the logs folder for details.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.log_message(f"An error occurred: {str(e)}")

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        # Ensure the log area scrolls to the end after each new message
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

def main():
    root = tk.Tk()
    gui = FileRenamerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
