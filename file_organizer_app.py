import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime

# -----------------------------
# ORGANIZE FUNCTION
# -----------------------------
def organize_files():
    folder_path = path_entry.get()

    if not folder_path:
        messagebox.showerror("Error", "Please select a folder!")
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    sort_option = sort_var.get()

    file_categories = {
        "Images": ["jpg", "jpeg", "png", "gif", "bmp"],
        "Videos": ["mp4", "mkv", "avi", "mov"],
        "Audio": ["mp3", "wav", "aac"],
        "Documents": ["pdf", "docx", "txt", "pptx", "xlsx"]
    }

    moved_count = 0

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        file_ext = filename.split(".")[-1].lower() if "." in filename else ""

        timestamp = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(timestamp).strftime("%B_%Y")

        if sort_option == "Sort by Type":
            folder_name = get_type_folder(file_ext, file_categories)

        elif sort_option == "Sort by Date":
            folder_name = file_date

        elif sort_option == "Sort by Type + Date":
            type_folder = get_type_folder(file_ext, file_categories)
            folder_name = f"{type_folder}_{file_date}"

        else:
            folder_name = "Others"

        target_folder = os.path.join(folder_path, folder_name)
        os.makedirs(target_folder, exist_ok=True)

        shutil.move(file_path, os.path.join(target_folder, filename))
        moved_count += 1

    status_label.config(text=f"✔ {moved_count} files organized successfully!", fg="#2ecc71")


def get_type_folder(extension, categories):
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return "Others"


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, END)
        path_entry.insert(0, folder_selected)


# -----------------------------
# MODERN UI DESIGN
# -----------------------------
root = Tk()
root.title("Smart File Organizer Pro")
root.geometry("600x420")
root.configure(bg="#1e272e")
root.resizable(False, False)

# Title
Label(root,
      text="Smart File Organizer",
      font=("Segoe UI", 24, "bold"),
      bg="#1e272e",
      fg="#ffffff").pack(pady=20)

# Main Card Frame
card = Frame(root, bg="#2f3640", padx=30, pady=30)
card.pack(pady=10)

# Folder Label
Label(card,
      text="Select Folder",
      font=("Segoe UI", 12),
      bg="#2f3640",
      fg="white").grid(row=0, column=0, sticky="w")

# Entry
path_entry = Entry(card,
                   width=40,
                   font=("Segoe UI", 11))
path_entry.grid(row=1, column=0, pady=10)

# Browse Button
Button(card,
       text="Browse",
       command=browse_folder,
       bg="#0984e3",
       fg="white",
       font=("Segoe UI", 10, "bold"),
       relief=FLAT,
       width=12).grid(row=1, column=1, padx=10)

# Sorting Option
Label(card,
      text="Sorting Option",
      font=("Segoe UI", 12),
      bg="#2f3640",
      fg="white").grid(row=2, column=0, sticky="w", pady=(20,0))

sort_var = StringVar()
sort_var.set("Sort by Type")

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox",
                fieldbackground="#ffffff",
                background="#ffffff")

sort_menu = ttk.Combobox(card,
                         textvariable=sort_var,
                         values=["Sort by Type",
                                 "Sort by Date",
                                 "Sort by Type + Date"],
                         state="readonly",
                         width=37)
sort_menu.grid(row=3, column=0, pady=10)

# Organize Button
Button(card,
       text="Organize Files",
       command=organize_files,
       bg="#00b894",
       fg="white",
       font=("Segoe UI", 12, "bold"),
       relief=FLAT,
       width=25).grid(row=4, column=0, pady=30)

# Status Label
status_label = Label(root,
                     text="Ready",
                     font=("Segoe UI", 10),
                     bg="#1e272e",
                     fg="#dfe6e9")
status_label.pack(pady=10)

root.mainloop()