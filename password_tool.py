import tkinter as tk
from tkinter import filedialog, messagebox, font
from zxcvbn import zxcvbn

# ----------- Password Functions -----------

leet_dict = {
    'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'],
    'o': ['0'], 's': ['$', '5'], 't': ['7']
}

def leetspeak(word):
    variants = set([word])
    word = word.lower()
    for i, c in enumerate(word):
        if c in leet_dict:
            for replacement in leet_dict[c]:
                variant = word[:i] + replacement + word[i+1:]
                variants.add(variant)
    return list(variants)

def append_years(word, years=range(1990, 2031)):
    return [f"{word}{year}" for year in years]

def generate_mutations(word):
    mutations = set()
    leet_versions = leetspeak(word)
    for variant in leet_versions:
        mutations.update(append_years(variant))
        mutations.add(variant)
    return mutations

def analyze_password(password: str) -> dict:
    result = zxcvbn(password)
    return {
        "score": result['score'],
        "feedback": result['feedback'],
        "crack_times": result['crack_times_display']
    }

def generate_wordlist(inputs: dict) -> list:
    base_words = [v for v in inputs.values() if v]
    wordlist = set()
    for word in base_words:
        wordlist.update(generate_mutations(word))
    return list(wordlist)

def save_wordlist(wordlist: list, filename="wordlist.txt"):
    if not filename:
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for word in wordlist:
                f.write(word + "\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save wordlist:\n{e}")

# ----------- GUI -----------

def run_gui():
    root = tk.Tk()
    root.title("🔐 Password Analyzer & Wordlist Generator")
    root.geometry("700x700")

    current_theme = 'dark'
    font_size = tk.IntVar(value=11)
    app_font = font.Font(family="Helvetica", size=font_size.get())

    save_path = tk.StringVar(value="wordlist.txt")
    wordlist_data = []

    themes = {
        'dark': {
            'bg': "#1e1e1e", 'fg': "#ffffff", 'entry_bg': "#2e2e2e",
            'btn_bg': "#444444", 'btn_fg': "#ffffff", 'active_bg': "#666666",
            'active_fg': "#ffffff"
        },
        'light': {
            'bg': "#ffffff", 'fg': "#000000", 'entry_bg': "#f0f0f0",
            'btn_bg': "#dcdcdc", 'btn_fg': "#000000", 'active_bg': "#cccccc",
            'active_fg': "#000000"
        }
    }

    widgets = []
    entries = []
    buttons = []

    def apply_theme(theme_name):
        theme = themes[theme_name]
        root.configure(bg=theme['bg'])

        for w in widgets:
            if isinstance(w, (tk.Label, tk.Checkbutton, tk.Scale)):
                w.configure(bg=theme['bg'], fg=theme['fg'], font=app_font)
            elif isinstance(w, tk.Frame):
                w.configure(bg=theme['bg'])

        for e in entries:
            e.configure(bg=theme['entry_bg'], fg=theme['fg'],
                        insertbackground=theme['fg'], font=app_font)

        for b in buttons:
            b.configure(
                bg=theme['btn_bg'], fg=theme['btn_fg'],
                activebackground=theme['active_bg'],
                activeforeground=theme['active_fg'],
                font=app_font
            )

        text_output.configure(bg=theme['entry_bg'], fg=theme['fg'],
                              insertbackground=theme['fg'], font=app_font)

    def make_label(text):
        lbl = tk.Label(root, text=text, anchor="w", font=app_font)
        lbl.pack(fill="x", padx=10, pady=2)
        widgets.append(lbl)
        return lbl

    def make_entry(secret=False):
        ent = tk.Entry(root, width=50, font=app_font)
        if secret:
            ent.config(show="*")
        ent.pack(padx=10, pady=3, fill="x")
        entries.append(ent)
        return ent

    def toggle_theme():
        nonlocal current_theme
        current_theme = 'light' if current_theme == 'dark' else 'dark'
        theme_btn.configure(text=f"🌗 Switch to {'Dark' if current_theme == 'light' else 'Light'} Mode")
        apply_theme(current_theme)

    def update_font_size(val):
        app_font.configure(size=int(val))
        apply_theme(current_theme)

    def browse_save_location():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="wordlist.txt",
            title="Choose save location"
        )
        if file_path:
            save_path.set(file_path)

    def analyze_and_generate():
        nonlocal wordlist_data

        password = entry_password.get()
        name = entry_name.get()
        dob = entry_dob.get()
        pet = entry_pet.get()

        if not password:
            messagebox.showerror("Input Error", "Password is required.")
            return

        result = analyze_password(password)
        feedback = result['feedback']
        crack_time = result['crack_times']['online_no_throttling_10_per_second']
        score = result['score']

        output = f"Password Score: {score}/4\n"
        output += f"Crack Time (Online): {crack_time}\n"
        output += f"Feedback: {feedback['warning'] or 'Looks okay'}\n"
        if feedback['suggestions']:
            output += f"Suggestions: {'; '.join(feedback['suggestions'])}\n"
        output += "\nGenerated Wordlist:\n"

        user_inputs = {"name": name, "dob": dob, "pet": pet}
        wordlist_data = generate_wordlist(user_inputs)
        wordlist_data.sort()

        output += "\n".join(wordlist_data)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

    def save_now():
        if not wordlist_data:
            messagebox.showerror("Nothing to Save", "Generate a wordlist first.")
            return
        save_wordlist(wordlist_data, filename=save_path.get())
        messagebox.showinfo("Saved", f"Wordlist saved to:\n{save_path.get()}")

    # --------- UI Setup ---------

    make_label("Password:")
    entry_password = make_entry(secret=True)

    make_label("Name:")
    entry_name = make_entry()

    make_label("Date of Birth (e.g. 1990):")
    entry_dob = make_entry()

    make_label("Pet Name:")
    entry_pet = make_entry()

    # Save Path
    save_frame = tk.Frame(root)
    save_frame.pack(fill="x", padx=10, pady=5)
    widgets.append(save_frame)

    save_label = tk.Label(save_frame, text="Save Location:")
    save_label.pack(side="left")
    widgets.append(save_label)

    save_entry = tk.Entry(save_frame, textvariable=save_path)
    save_entry.pack(side="left", fill="x", expand=True, padx=5)
    entries.append(save_entry)

    browse_button = tk.Button(save_frame, text="Browse", command=browse_save_location)
    browse_button.pack(side="right")
    buttons.append(browse_button)

    # Theme button
    theme_btn = tk.Button(root, text="🌗 Switch to Light Mode", command=toggle_theme)
    theme_btn.pack(pady=5)
    buttons.append(theme_btn)

    # Font size slider
    make_label("Font Size:")
    font_slider = tk.Scale(root, from_=8, to=20, orient="horizontal",
                           variable=font_size, command=update_font_size)
    font_slider.pack(fill="x", padx=10)
    widgets.append(font_slider)

    # Analyze and Generate Button
    analyze_btn = tk.Button(root, text="Analyze & Generate Wordlist", command=analyze_and_generate)
    analyze_btn.pack(pady=5)
    buttons.append(analyze_btn)

    # Save Button
    save_btn = tk.Button(root, text="💾 Save Wordlist", command=save_now)
    save_btn.pack(pady=5)
    buttons.append(save_btn)

    # Output Text Box
    text_output = tk.Text(root, height=15, font=app_font)
    text_output.pack(padx=10, pady=10, fill="both", expand=True)

    # Apply initial theme
    apply_theme(current_theme)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
