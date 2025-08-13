import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, insert_expense, get_all_expenses, get_expenses_by_category
from utils import get_today

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")

        self.create_widgets()
        self.refresh_expense_table()

    def create_widgets(self):
        # Form
        form_frame = tk.Frame(self.root, pady=10)
        form_frame.pack()

        tk.Label(form_frame, text="Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(form_frame)
        self.category_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Description:").grid(row=2, column=0)
        self.description_entry = tk.Entry(form_frame)
        self.description_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=3, column=1)
        self.date_entry.insert(0, get_today())

        tk.Button(form_frame, text="Add Expense", command=self.add_expense).grid(row=4, columnspan=2, pady=10)

        # Tabs
        self.tab_control = ttk.Notebook(self.root)

        self.all_expenses_tab = ttk.Frame(self.tab_control)
        self.by_category_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.all_expenses_tab, text='All Expenses')
        self.tab_control.add(self.by_category_tab, text='By Category')
        self.tab_control.pack(expand=1, fill="both")

        # Tables
        self.expense_tree = ttk.Treeview(self.all_expenses_tab, columns=("ID", "Amount", "Category", "Description", "Date"), show='headings')
        for col in ("ID", "Amount", "Category", "Description", "Date"):
            self.expense_tree.heading(col, text=col)
            self.expense_tree.column(col, width=100)
        self.expense_tree.pack(expand=1, fill="both")

        self.category_tree = ttk.Treeview(self.by_category_tab, columns=("Category", "Total"), show='headings')
        for col in ("Category", "Total"):
            self.category_tree.heading(col, text=col)
            self.category_tree.column(col, width=200)
        self.category_tree.pack(expand=1, fill="both")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            date = self.date_entry.get()

            if not category or not date:
                raise ValueError("Category and date are required.")

            insert_expense(amount, category, description, date)
            messagebox.showinfo("Success", "Expense added!")
            self.clear_form()
            self.refresh_expense_table()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, get_today())

    def refresh_expense_table(self):
        # All Expenses
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)
        for row in get_all_expenses():
            self.expense_tree.insert('', tk.END, values=row)

        # By Category
        for row in self.category_tree.get_children():
            self.category_tree.delete(row)
        for row in get_expenses_by_category():
            self.category_tree.insert('', tk.END, values=row)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
