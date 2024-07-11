import tkinter as tk
from tkinter import filedialog
import subprocess

# Tạo cửa sổ chính
root = tk.Tk()
root.title('Hướng dẫn')

# Hàm để chạy file Python khác
def run_tutorial(file_name):
    try:
        # Sử dụng subprocess để chạy file Python khác
        subprocess.run(["python", file_name])
    except Exception as e:
        print(f"Error: {e}")

tutorial_1=tk.Button(root, text="Hướng dẫn nốt Do , Re , Mi", command=lambda : run_tutorial ("Basics\testing 1st tutorial.py"))
tutorial_1.pack(pady=10)

tutorial_2=tk.Button(root, text="Hướng dẫn nốt Fa, Sol", command=lambda : run_tutorial ("Basics\testing 2nd tutorial.py"))
tutorial_2.pack(pady=10)

tutorial_3=tk.Button(root, text="Kiểm tra lại 5 nốt", command=lambda : run_tutorial ("Basics\testing 3rd tutorial.py"))
tutorial_3.pack(pady=10)

root.mainloop()