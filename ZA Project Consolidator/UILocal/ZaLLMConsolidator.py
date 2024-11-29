import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os


def get_file_info(filepath):
    """Collects file information."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        size = os.path.getsize(filepath)
        num_lines = len(lines)
        relative_path = os.path.relpath(filepath, folder_path)
        tree = relative_path.replace(os.sep, " > ")
        return {
            "name": os.path.basename(filepath),
            "path": filepath,
            "relative_path": relative_path,
            "tree": tree,
            "size": size,
            "lines": num_lines,
            "content": content,
        }
    except Exception as e:
        return {"error": str(e)}


def process_folder(folder_path):
    """Processes the selected folder and consolidates file content."""
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder.")
        return

    text_area.delete("1.0", tk.END)  # Clear previous content

    try:
        with open("consolidated_project.txt", "w", encoding="utf-8") as outfile:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    filepath = os.path.join(root, file)
                    info = get_file_info(filepath)

                    if "error" in info:
                        text_area.insert(
                            tk.END, f"Error reading {filepath}: {info['error']}\n"
                        )
                        outfile.write(f"Error reading {filepath}: {info['error']}\n")
                    else:
                        outfile.write("=" * 72 + "\n")
                        outfile.write(f"Name: {info['name']}\n")
                        outfile.write(f"Location: {info['path']}\n")
                        outfile.write(f"Tree: {info['tree']}\n")
                        outfile.write(f"Size: {info['size']} bytes\n")
                        outfile.write(f"Lines: {info['lines']}\n")
                        outfile.write("\nContent:\n")
                        outfile.write(info["content"] + "\n")

                        text_area.insert(
                            tk.END, f"Processed: {info['relative_path']}\n"
                        )
        text_area.insert(tk.END, "\nConsolidation complete: consolidated_project.txt\n")
        messagebox.showinfo("Success", "Project consolidated successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def browse_folder():
    """Opens dialog to select a folder."""
    global folder_path
    folder_path = filedialog.askdirectory()
    path_label.config(text=folder_path)


# GUI setup
root = tk.Tk()
root.title("Project Consolidator")
folder_path = ""

# Folder selection
tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=20)
path_label = tk.Label(root, text="No folder selected")
path_label.pack(pady=10)

# Process button
tk.Button(
    root, text="Consolidate Project", command=lambda: process_folder(folder_path)
).pack(pady=20)

# Text area for output
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_area.pack(pady=20)

root.mainloop()
