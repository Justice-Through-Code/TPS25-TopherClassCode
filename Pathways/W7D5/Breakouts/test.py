import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
window = tk.Tk()
window.title("Student Registration Form")
window.geometry("500x400")
window.configure(bg="darkgray")
window.resizable(True, True)

title_label = tk.Label(
    window,
    text="Welcome To Hoosegow U",
    font=("Tahoma", 18, "bold"),
    bg= "lightblue"
)
title_label.pack(pady=20)

form_frame = tk.Frame(window, bg="darkgray")
form_frame.pack(pady=20)

name_label = tk.Label(form_frame, text="Name:", font=("Tahoma", 12), bg="darkgray", fg="white")
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1)

window.mainloop()