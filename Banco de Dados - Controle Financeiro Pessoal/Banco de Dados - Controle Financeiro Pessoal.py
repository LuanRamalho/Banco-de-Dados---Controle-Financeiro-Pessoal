import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Função para salvar dados em um arquivo JSON
def save_data(data, filename='finance_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Função para carregar dados de um arquivo JSON
def load_data(filename='finance_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {"expenses": [], "incomes": []}

# Função para adicionar uma despesa
def add_expense():
    try:
        expense_amount = float(expense_entry.get())
        expense_description = expense_desc_entry.get()
        data["expenses"].append({"amount": expense_amount, "description": expense_description})
        save_data(data)
        expense_entry.delete(0, tk.END)
        expense_desc_entry.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

# Função para adicionar uma receita
def add_income():
    try:
        income_amount = float(income_entry.get())
        income_description = income_desc_entry.get()
        data["incomes"].append({"amount": income_amount, "description": income_description})
        save_data(data)
        income_entry.delete(0, tk.END)
        income_desc_entry.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Receita adicionada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")

# Função para gerar gráficos
def generate_graphs():
    expenses = sum(expense["amount"] for expense in data["expenses"])
    incomes = sum(income["amount"] for income in data["incomes"])
    labels = ['Despesas', 'Receitas']
    values = [expenses, incomes]
    colors = ['#ff9999', '#66b3ff']

    # Função para criar etiquetas personalizadas
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}%\nR$ {val:,}'
        return my_autopct

    plt.figure(figsize=(10, 5))
    plt.pie(values, labels=labels, colors=colors, autopct=make_autopct(values), startangle=90)
    plt.title('Distribuição de Despesas e Receitas')
    plt.show()

# Função para gerar relatório
def generate_report():
    report = tk.Toplevel(root)
    report.title("Relatório Financeiro")
    report.configure(bg='#640098')  

    total_expenses = sum(expense["amount"] for expense in data["expenses"])
    total_incomes = sum(income["amount"] for income in data["incomes"])
    balance = total_incomes - total_expenses

    report_text = f"Total de Despesas: R$ {total_expenses:.2f}\nTotal de Receitas: R$ {total_incomes:.2f}\nSaldo: R$ {balance:.2f}"
    
    # Título do relatório
    title_label = tk.Label(report, text="Relatório Financeiro", font=('Helvetica', 16, 'bold'), bg='#640098', fg='white')
    title_label.pack(pady=(10, 20))

    # Texto do relatório
    report_label = tk.Label(report, text=report_text, font=('Helvetica', 12), padx=20, pady=20, bg='#ffffff', fg='#333', bd=2, relief='solid')
    report_label.pack(padx=20, pady=10)

    # Botão para salvar PDF
    save_pdf_button = tk.Button(report, text="Salvar Relatório em PDF", command=lambda: save_report_pdf(report_text), bg='#4CAF50', fg='white', font=('Helvetica', 12, "bold"), bd=2, relief='raised')
    save_pdf_button.pack(pady=10)

# Função para salvar relatório em PDF
def save_report_pdf(report_text):
    c = canvas.Canvas("relatorio_financeiro.pdf", pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, report_text)
    c.save()
    messagebox.showinfo("Sucesso", "Relatório salvo como PDF!")

# Função para exibir despesas e receitas em uma nova janela
def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Ver Registros")
    records_window.configure(bg='white')

    expenses_frame = tk.Frame(records_window, bg='lightblue', padx=10, pady=10)
    expenses_frame.pack(fill='x')
    expenses_label = tk.Label(expenses_frame, text="Despesas", bg='lightblue', font=("Arial", 15, "bold"))
    expenses_label.pack(fill='x')
    for i, expense in enumerate(data["expenses"]):
        record_frame = tk.Frame(expenses_frame, bg='lightblue')
        record_frame.pack(fill='x', padx=10, pady=5)
        record_label = tk.Label(record_frame, text=f"{i+1}. {expense['description']}: R$ {expense['amount']:.2f}", bg='lightblue', font=("Helvetica", 14))
        record_label.pack(side='left', padx=5)
        edit_button = tk.Button(record_frame, text="Editar", command=lambda i=i: edit_expense(i), font=("Arial", 12, "bold"), bg='#005D23', fg="white")
        edit_button.pack(side='right')
        delete_button = tk.Button(record_frame, text="Excluir", command=lambda i=i: delete_expense(i), font=("Arial", 12, "bold"), bg='#EF0202', fg="white")
        delete_button.pack(side='right')

    incomes_frame = tk.Frame(records_window, bg='lightgreen', padx=10, pady=10)
    incomes_frame.pack(fill='x')
    incomes_label = tk.Label(incomes_frame, text="Receitas", bg='lightgreen' , font=("Arial", 15, "bold"))
    incomes_label.pack(fill='x')
    for i, income in enumerate(data["incomes"]):
        record_frame = tk.Frame(incomes_frame, bg='lightgreen')
        record_frame.pack(fill='x', padx=10, pady=5)
        record_label = tk.Label(record_frame, text=f"{i+1}. {income['description']}: R$ {income['amount']:.2f}", bg='lightgreen' , font=("Helvetica", 14))
        record_label.pack(side='left', padx=5)
        edit_button = tk.Button(record_frame, text="Editar", command=lambda i=i: edit_income(i), font=("Arial", 12, "bold"), bg='#005D23', fg="white")
        edit_button.pack(side='right')
        delete_button = tk.Button(record_frame, text="Excluir", command=lambda i=i: delete_income(i), font=("Arial", 12, "bold"), bg='#EF0202', fg="white")
        delete_button.pack(side='right')

# Função para editar uma despesa
def edit_expense(index):
    new_description = simpledialog.askstring("Editar Despesa", "Descrição:", initialvalue=data["expenses"][index]["description"])
    new_amount = simpledialog.askfloat("Editar Despesa", "Valor:", initialvalue=data["expenses"][index]["amount"])
    if new_description and new_amount is not None:
        data["expenses"][index] = {"amount": new_amount, "description": new_description}
        save_data(data)
        messagebox.showinfo("Sucesso", "Despesa editada com sucesso!")
        view_records()

# Função para editar uma receita
def edit_income(index):
    new_description = simpledialog.askstring("Editar Receita", "Descrição:", initialvalue=data["incomes"][index]["description"])
    new_amount = simpledialog.askfloat("Editar Receita", "Valor:", initialvalue=data["incomes"][index]["amount"])
    if new_description and new_amount is not None:
        data["incomes"][index] = {"amount": new_amount, "description": new_description}
        save_data(data)
        messagebox.showinfo("Sucesso", "Receita editada com sucesso!")
        view_records()

# Função para excluir uma despesa
def delete_expense(index):
    if messagebox.askyesno("Excluir Despesa", "Você tem certeza que deseja excluir esta despesa?"):
        data["expenses"].pop(index)
        save_data(data)
        messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")
        view_records()  # Atualiza a janela de registros

# Função para excluir uma receita
def delete_income(index):
    if messagebox.askyesno("Excluir Receita", "Você tem certeza que deseja excluir esta receita?"):
        data["incomes"].pop(index)
        save_data(data)
        messagebox.showinfo("Sucesso", "Receita excluída com sucesso!")
        view_records()  # Atualiza a janela de registros

# Carregar os dados existentes
data = load_data()

# Criar a interface gráfica principal
root = tk.Tk()
root.title("Gerenciador de Finanças Pessoais")
root.configure(bg='white')

# Seção de Despesas
expense_frame = tk.Frame(root, padx=10, pady=10, bg='lightblue')
expense_frame.pack(fill='x')
expense_label = tk.Label(expense_frame, text="Adicionar Despesa", bg='lightblue' , font=("Arial", 15, "bold"))
expense_label.pack()
expense_desc_entry = tk.Entry(expense_frame, width=50)
expense_desc_entry.pack(pady=5)
expense_entry = tk.Entry(expense_frame, width=20)
expense_entry.pack(pady=5)
expense_button = tk.Button(expense_frame, text="Adicionar", command=add_expense, font=("Arial", 12, "bold"), bg='#96A400', fg="white")
expense_button.pack(pady=5)

# Seção de Receitas
income_frame = tk.Frame(root, padx=10, pady=10, bg='lightgreen')
income_frame.pack(fill='x')
income_label = tk.Label(income_frame, text="Adicionar Receita", bg='lightgreen' ,  font=("Arial", 15, "bold"))
income_label.pack()
income_desc_entry = tk.Entry(income_frame, width=50)
income_desc_entry.pack(pady=5)
income_entry = tk.Entry(income_frame, width=20)
income_entry.pack(pady=5)
income_button = tk.Button(income_frame, text="Adicionar", command=add_income, font=("Arial", 12, "bold"), bg='#96A400', fg="white")
income_button.pack(pady=5)

# Botões de Gráficos e Relatórios
buttons_frame = tk.Frame(root, padx=10, pady=10, bg='white')
buttons_frame.pack(fill='x')
graph_button = tk.Button(buttons_frame, text="Gerar Gráficos", command=generate_graphs, font=("Arial", 12, "bold"), bg='#005D23', fg="white")
graph_button.pack(side='left', padx=5)
report_button = tk.Button(buttons_frame, text="Gerar Relatório", command=generate_report, font=("Arial", 12, "bold"), bg='#AA0098', fg="white")
report_button.pack(side='left', padx=5)
view_records_button = tk.Button(buttons_frame, text="Ver Registros", command=view_records, font=("Arial", 12, "bold"), bg='#0067DB', fg="white")
view_records_button.pack(side='left', padx=5)

root.mainloop()
