import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip


def generate_password():
    try:
        length = int(length_entry.get())
        if length < 8 or length > 128:
            messagebox.showerror("Error", "❗ Password length must be between 8 and 128.")
            return

        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()
        exclude_similar = exclude_similar_var.get()

        characters = ""
        if use_letters:
            characters += string.ascii_letters
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "❗ At least one character type must be selected.")
            return

        if exclude_similar:
           
            similar_characters = "il1Lo0O"
            characters = "".join([c for c in characters if c not in similar_characters])

        password = "".join(random.choice(characters) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        
        update_strength_indicator(password)

       
        password_history.insert(0, password)
        if password_history.size() > 10: 
            password_history.delete(10)

    except ValueError:
        messagebox.showerror("Error", "❗ Invalid input. Please enter a valid number.")


def update_strength_indicator(password):
    strength = 0
    if len(password) >= 12:
        strength += 1
    if any(c in string.ascii_uppercase for c in password):
        strength += 1
    if any(c in string.digits for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    strength_indicator["value"] = strength * 25  
    if strength <= 2:
        strength_indicator["style"] = "red.Horizontal.TProgressbar"
    elif strength == 3:
        strength_indicator["style"] = "yellow.Horizontal.TProgressbar"
    else:
        strength_indicator["style"] = "green.Horizontal.TProgressbar"


def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "✅ Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "❗ No password generated yet.")


def save_passwords():
    passwords = password_history.get(0, tk.END)
    if not passwords:
        messagebox.showerror("Error", "❗ No passwords generated yet.")
        return

    with open("passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    messagebox.showinfo("Success", "✅ Passwords saved to 'passwords.txt'.")


root = tk.Tk()
root.title("🔐 Enhanced Password Generator")


tk.Label(root, text="Password Length (8-128):").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)
length_entry.insert(0, "12")  

letters_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Letters", variable=letters_var).grid(row=1, column=0, columnspan=2, sticky="w")

numbers_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, columnspan=2, sticky="w")

symbols_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(row=3, column=0, columnspan=2, sticky="w")

exclude_similar_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Exclude Similar Characters (e.g., i, l, 1, o, 0)", variable=exclude_similar_var).grid(row=4, column=0, columnspan=2, sticky="w")

tk.Button(root, text="Generate Password", command=generate_password).grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(root, text="Generated Password:").grid(row=6, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=6, column=1, padx=10, pady=10)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=7, column=0, columnspan=2, pady=10)


tk.Label(root, text="Password Strength:").grid(row=8, column=0, padx=10, pady=10)
style = ttk.Style()
style.theme_use("clam")
style.configure("red.Horizontal.TProgressbar", background="red")
style.configure("yellow.Horizontal.TProgressbar", background="yellow")
style.configure("green.Horizontal.TProgressbar", background="green")
strength_indicator = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
strength_indicator.grid(row=8, column=1, padx=10, pady=10)


tk.Label(root, text="Password History:").grid(row=9, column=0, padx=10, pady=10)
password_history = tk.Listbox(root, height=5, width=30)
password_history.grid(row=9, column=1, padx=10, pady=10)


tk.Button(root, text="Save Passwords to File", command=save_passwords).grid(row=10, column=0, columnspan=2, pady=10)


root.mainloop()
