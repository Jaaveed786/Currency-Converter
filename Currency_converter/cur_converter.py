from bs4 import BeautifulSoup
from decimal import Decimal
import requests, os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class MainApplication(tk.Frame):
    font = ('Arial', 18, 'bold')  # Increased font size
    precision = 4
    themes = ["light", "dark", "blue", "green", "purple"]
    theme_index = 0

    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.window = window
        self.Names, self.Values = [], []
        self.setup_appearance()
        self.setup_widgets()
        self.apply_theme(self.themes[self.theme_index])

    def setup_appearance(self):
        """Setup window properties"""
        self.window.title("Currency Converter")
        self.window.geometry("800x600")  # Increased window size
        self.window.resizable(False, False)
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass

    def convert(self):
        """Perform currency conversion"""
        self.print_num()
        number = Decimal(self.textbox_amount.get("1.0", tk.END).strip() or 0)
        index_from = self.Names.index(self.from_box.get())
        index_to = self.Names.index(self.to_box.get())
        number *= Decimal(self.Values[index_to]) / Decimal(self.Values[index_from])

        self.textbox_output.config(state=tk.NORMAL)
        self.textbox_output.delete("1.0", tk.END)
        self.textbox_output.insert(tk.END, round(number, self.precision))
        self.textbox_output.config(state=tk.DISABLED)

    def print_num(self):
        """Clean and format input"""
        number = ''.join([i if i.isdigit() or i == '.' else '' for i in self.textbox_amount.get("1.0", tk.END)])
        number = float(number) if number else 0
        self.textbox_amount.delete("1.0", tk.END)
        self.textbox_amount.insert(tk.END, round(Decimal(number), self.precision))

    def get_exchange_rates(self):
        """Fetch live exchange rates"""
        exchanges = [["US Dollar", "1"]]
        try:
            text = requests.get("https://www.x-rates.com/table/?from=USD&amount=1")
            soup = BeautifulSoup(text.content, 'lxml')
            for tr_tag in soup.find_all('tbody')[1]:
                try:
                    td_tags = tr_tag.find_all('td')
                    exchanges.append([td_tags[0].text, td_tags[1].text])
                except:
                    pass
            exchanges.sort()
        except:
            if os.path.isfile('data.txt'):
                with open('data.txt', 'r') as f:
                    exchanges = [line.split(',') for line in f.read().split('|')]
        return exchanges

    def setup_widgets(self):
        """Setup UI elements"""
        exchanges = self.get_exchange_rates()
        self.Names, self.Values = zip(*exchanges)

        # Labels (Left-aligned)
        self.amount_label = tk.Label(self.window, text="Amount:", font=self.font, anchor="w")
        self.from_label = tk.Label(self.window, text="From:", font=self.font, anchor="w")
        self.to_label = tk.Label(self.window, text="To:", font=self.font, anchor="w")
        self.output_label = tk.Label(self.window, text="Converted:", font=self.font, anchor="w")

        # Textboxes (Left-aligned, Larger Size)
        self.textbox_amount = tk.Text(self.window, height=2, width=40, font=self.font)
        self.textbox_output = tk.Text(self.window, height=2, width=40, font=self.font, state=tk.DISABLED)

        # Dropdowns (Larger Size)
        self.from_box = ttk.Combobox(self.window, values=self.Names, font=self.font, width=36)
        self.to_box = ttk.Combobox(self.window, values=self.Names, font=self.font, width=36)
        self.from_box.current(0)
        self.to_box.current(0)

        # Convert Button (Larger Size)
        self.convert_button = tk.Button(self.window, text="Convert", command=self.convert, font=self.font, width=22)

        # Load Theme Button Icon
        try:
            self.theme_icon = Image.open("theme_icon.png").resize((40, 40))
            self.theme_icon = ImageTk.PhotoImage(self.theme_icon)
        except:
            self.theme_icon = None

            # Small Round Theme Toggle Button (Left Bottom Corner)
        if self.theme_icon:
            self.theme_button = tk.Button(self.window, image=self.theme_icon, command=self.toggle_theme, borderwidth=0)
        else:
            self.theme_button = tk.Button(self.window, text="⚫", command=self.toggle_theme, font=("Arial", 14, "bold"),
                                          width=3, height=1)

        # Grid Layout (Left-aligned, Adjusted Spacing)
        self.amount_label.grid(row=0, column=0, sticky=tk.W, padx=30, pady=10)
        self.textbox_amount.grid(row=1, column=0, padx=30, pady=10)

        self.from_label.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)
        self.from_box.grid(row=3, column=0, padx=30, pady=10)

        self.to_label.grid(row=4, column=0, sticky=tk.W, padx=30, pady=10)
        self.to_box.grid(row=5, column=0, padx=30, pady=10)

        self.output_label.grid(row=6, column=0, sticky=tk.W, padx=30, pady=10)
        self.textbox_output.grid(row=7, column=0, padx=30, pady=10)

        self.convert_button.grid(row=8, column=0, pady=20)

        # Move theme toggle button to bottom-left
        self.theme_button.place(x=30, y=540)

    def toggle_theme(self):
        """Switch Themes"""
        self.theme_index = (self.theme_index + 1) % len(self.themes)
        self.apply_theme(self.themes[self.theme_index])

    def apply_theme(self, theme):
        """Apply Theme to UI Elements"""
        theme_colors = {
            "light": {"bg": "white", "fg": "black", "btn": "gray", "text_bg": "white", "text_fg": "black"},
            "dark": {"bg": "#2E2E2E", "fg": "white", "btn": "#444444", "text_bg": "black", "text_fg": "white"},
            "blue": {"bg": "#1E3A8A", "fg": "white", "btn": "#3B82F6", "text_bg": "#93C5FD", "text_fg": "black"},
            "green": {"bg": "#065F46", "fg": "white", "btn": "#10B981", "text_bg": "#A7F3D0", "text_fg": "black"},
            "purple": {"bg": "#6B21A8", "fg": "white", "btn": "#A855F7", "text_bg": "#E9D5FF", "text_fg": "black"},
        }

        colors = theme_colors.get(theme, theme_colors["light"])

        self.window.config(bg=colors["bg"])
        for widget in [self.amount_label, self.from_label, self.to_label, self.output_label]:
            widget.config(bg=colors["bg"], fg=colors["fg"])

        for text_box in [self.textbox_amount, self.textbox_output]:
            text_box.config(bg=colors["text_bg"], fg=colors["text_fg"])

        self.convert_button.config(bg=colors["btn"], fg="white")
        self.theme_button.config(bg=colors["btn"])


# Run App
if __name__ == "__main__":
    window = tk.Tk()
    app = MainApplication(window)
    window.mainloop()
