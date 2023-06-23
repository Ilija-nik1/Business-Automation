import tkinter as tk
import requests

class CurrencyConverter:
    def __init__(self, url):
        data = requests.get(url).json()
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != "USD":
            amount = amount / self.rates[from_currency]
        # limiting the precision to 4 decimal places
        amount = round(amount * self.rates[to_currency], 4)
        return amount

class App(tk.Frame):
    currencies = {
        "USD": "$",
        "EUR": "€",
        "JPY": "¥",
        "GBP": "£",
        "AUD": "$",
        "CAD": "$",
        "CHF": "CHF",
        "CNY": "¥",
        "HKD": "$",
        "NZD": "$"
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.refresh_rates()

    def create_widgets(self):
        self.amount_label = tk.Label(self, text="Amount:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=0, column=1)

        self.from_label = tk.Label(self, text="From:")
        self.from_label.grid(row=1, column=0)
        self.from_var = tk.StringVar(self)
        self.from_var.set("USD")
        self.from_menu = tk.OptionMenu(self, self.from_var, *[(code + " " + self.currencies[code]) for code in self.currencies])
        self.from_menu.grid(row=1, column=1)

        self.to_label = tk.Label(self, text="To:")
        self.to_label.grid(row=2, column=0)
        self.to_var = tk.StringVar(self)
        self.to_var.set("EUR")
        self.to_menu = tk.OptionMenu(self, self.to_var, *[(code + " " + self.currencies[code]) for code in self.currencies])
        self.to_menu.grid(row=2, column=1)

        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        self.convert_button.grid(row=3, column=0)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=3, column=1)

        self.update_button = tk.Button(self, text="Update Currencies", command=self.update_currencies)
        self.update_button.grid(row=4, column=0, columnspan=2)

    def convert(self):
        amount_str = self.amount_entry.get()
        if not amount_str:
            self.result_label.config(text="Please enter an amount")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            self.result_label.config(text="Invalid amount")
            return

        from_currency = self.from_var.get().split()[0]
        to_currency = self.to_var.get().split()[0]
        if from_currency == to_currency:
            self.result_label.config(text="Please select different currencies")
            return

        converter = CurrencyConverter(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        converted_amount = converter.convert(from_currency, to_currency, amount)

        self.result_label.config(text=f"{self.currencies[to_currency]}{converted_amount:.2f}")

    def update_currencies(self):
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        if response.status_code == 200:
            data = response.json()
            self.currencies = data["rates"]
            self.from_menu['menu'].delete(0, 'end')
            self.to_menu['menu'].delete(0, 'end')
            for code in self.currencies:
                self.from_menu['menu'].add_command(label=code + " " + self.currencies[code], command=tk._setit(self.from_var, code))
                self.to_menu['menu'].add_command(label=code + " " + self.currencies[code], command=tk._setit(self.to_var, code))
            self.from_var.set("USD")
            self.to_var.set("EUR")
            self.result_label.config(text="Currencies updated successfully")
        else:
            self.result_label.config(text="Failed to update currencies")

    def refresh_rates(self):
        self.update_currencies()
        self.master.after(3600000, self.refresh_rates)

root = tk.Tk()
app = App(master=root)
app.mainloop()