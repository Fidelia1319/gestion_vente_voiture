import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import add_client, get_clients, update_client, delete_client, add_car, get_cars, update_car, delete_car, \
    add_purchase, get_purchases, update_purchase, delete_purchase, search_purchases, calculate_monthly_revenue, \
    add_revenue, connect
from invoice import generate_invoice
from ttkthemes import ThemedTk
import os
import webbrowser

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def validate_name(name):
    return all(c.isalpha() or c.isspace() for c in name)

def validate_purchase_num(purchase_num):
    return purchase_num.isdigit()

def create_main_window():
    global root, client_tree, car_tree, purchase_tree, purchase_client_id_entry, purchase_car_id_entry
    root = ThemedTk(theme="clam")
    root.title("Car Sales Management")
    root.geometry("1200x700")
    root.configure(bg='#e6f0fa')

    style = ttk.Style()
    style.theme_use("clam")

    # Couleurs et styles fidelia
    style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=6, background='#007BFF', foreground='white')
    style.map('TButton', background=[('active', '#0056b3')], foreground=[('active', 'white')])
    style.configure('TLabel', background='#e6f0fa', font=('Helvetica', 12), foreground='#007BFF')
    style.configure('TEntry', font=('Helvetica', 12))
    style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'), background='#007BFF', foreground='white')
    style.configure('Treeview', font=('Helvetica', 12), background='#e6f0fa', foreground='black', fieldbackground='#e6f0fa')
    style.configure('Red.TButton', background='#DC3545', foreground='white', font=('Helvetica', 12, 'bold'))
    style.map('Red.TButton', background=[('active', '#a71d2a')], foreground=[('active', 'white')])

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    tab_client = ttk.Frame(tab_control)
    tab_car = ttk.Frame(tab_control)
    tab_purchase = ttk.Frame(tab_control)
    tab_reports = ttk.Frame(tab_control)

    tab_control.add(tab_client, text='Clients', padding=10)
    tab_control.add(tab_car, text='Cars', padding=10)
    tab_control.add(tab_purchase, text='Purchases', padding=10)
    tab_control.add(tab_reports, text='Reports', padding=10)

    create_client_tab(tab_client)
    create_car_tab(tab_car)
    create_purchase_tab(tab_purchase)
    create_reports_tab(tab_reports)

    tab_control.bind("<<NotebookTabChanged>>", lambda event: refresh_all())

    # Barre de menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=on_closing)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Car Sales Management System v1.0"))

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def refresh_all():
    refresh_client_list()
    refresh_car_list()
    refresh_purchase_list()
    refresh_client_combobox()
    refresh_car_combobox()

def refresh_client_list():
    for row in client_tree.get_children():
        client_tree.delete(row)
    for client in get_clients():
        client_tree.insert("", "end", values=client)

def refresh_car_list():
    for row in car_tree.get_children():
        car_tree.delete(row)
    for car in get_cars():
        car_tree.insert("", "end", values=car)

def get_client_name(idcli):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT nom FROM client WHERE idcli = %s", (idcli,))
        result = cursor.fetchone()
        if result:
            nom = result[0]
        else:
            nom = "Client inconnu"
    except Exception as e:
        print(f"Error getting client name: {e}")
        nom = "Client inconnu"

    connection.close()
    return nom

def get_car_design(idvoit):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT design FROM voiture WHERE idvoit = %s", (idvoit,))
        result = cursor.fetchone()
        if result:
            design = result[0]
        else:
            design = "Voiture inconnue"
    except Exception as e:
        print(f"Error getting car design: {e}")
        design = "Voiture inconnue"

    connection.close()
    return design

def refresh_purchase_list():
    for row in purchase_tree.get_children():
        purchase_tree.delete(row)
    for purchase in get_purchases():
        idcli = purchase[1]
        idvoit = purchase[2]

        nom = get_client_name(idcli)
        design = get_car_design(idvoit)
        purchase_tree.insert("", "end", values=(purchase[0], nom, design, purchase[3], purchase[4]))

def refresh_client_combobox():
    clients = get_clients()
    client_names = [client[1] for client in clients]
    purchase_client_id_entry['values'] = client_names
    print("Updated client combobox with values: ", client_names)  # Debugging

def refresh_car_combobox():
    cars = get_cars()
    car_designs = [car[1] for car in cars]
    purchase_car_id_entry['values'] = car_designs
    print("Updated car combobox with values: ", car_designs)  # Debugging

def clear_fields(entries):
    for entry in entries:
        entry.delete(0, tk.END)

def validate_contact(contact):
    return contact.isdigit()

def validate_quantity(quantity):
    return quantity.isdigit()

def validate_price(price):
    return price.isdigit()

def create_client_tab(tab):
    global client_tree
    ttk.Label(tab, text="Client ID:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
    client_id_entry = ttk.Entry(tab)
    client_id_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Name:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
    client_name_entry = ttk.Entry(tab)
    client_name_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Contact:").grid(column=0, row=2, padx=10, pady=10, sticky='w')
    client_contact_entry = ttk.Entry(tab)
    client_contact_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

    def add_client_button():
        clients = get_clients()
        client_ids = [client[0] for client in clients]
        client_contacts = [client[2] for client in clients]

        if not (client_id_entry.get() and client_name_entry.get() and client_contact_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_name(client_name_entry.get()):
            messagebox.showwarning("Warning", "Le nom doit être uniquement composé de lettres")
            return
        if not validate_contact(client_contact_entry.get()):
            messagebox.showwarning("Warning", "Le contact doit être uniquement composé de chiffres")
            return
        if client_id_entry.get() in client_ids:
            messagebox.showwarning("Warning", "L'ID du client existe déjà")
            return
        if client_contact_entry.get() in client_contacts:
            messagebox.showwarning("Warning", "Le contact existe déjà pour un autre client")
            return
        result = add_client(client_id_entry.get(), client_name_entry.get(), client_contact_entry.get())
        messagebox.showinfo("Info", result)
        refresh_all()
        clear_fields([client_id_entry, client_name_entry, client_contact_entry])
        refresh_client_combobox()

    def update_client_button():
        if not client_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        clients = get_clients()
        selected_item = client_tree.selection()[0]
        selected_client = client_tree.item(selected_item, 'values')
        client_ids = [client[0] for client in clients if client[0] != selected_client[0]]
        client_contacts = [client[2] for client in clients if client[0] != selected_client[0]]

        if client_id_entry.get() != selected_client[0]:
            messagebox.showwarning("Warning", "L'ID du client ne peut pas être modifié")
            client_id_entry.delete(0, tk.END)
            client_id_entry.insert(0, selected_client[0])
            return

        if not (client_id_entry.get() and client_name_entry.get() and client_contact_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_name(client_name_entry.get()):
            messagebox.showwarning("Warning", "Le nom doit être uniquement composé de lettres")
            return
        if not validate_contact(client_contact_entry.get()):
            messagebox.showwarning("Warning", "Le contact doit être uniquement composé de chiffres")
            return
        if client_contact_entry.get() in client_contacts:
            messagebox.showwarning("Warning", "Le contact existe déjà pour un autre client")
            return
        result = update_client(client_id_entry.get(), client_name_entry.get(), client_contact_entry.get())
        messagebox.showinfo("Info", result)
        refresh_all()
        clear_fields([client_id_entry, client_name_entry, client_contact_entry])

    def delete_client_button():
        if not client_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        selected_items = client_tree.selection()
        for selected_item in selected_items:
            selected_client = client_tree.item(selected_item, 'values')
            if any(purchase[1] == selected_client[0] for purchase in get_purchases()):
                messagebox.showwarning("Warning", "Veuillez d'abord supprimer les achats de ce client")
                return
            delete_client(selected_client[0])
        messagebox.showinfo("Info", "Clients supprimés avec succès")
        refresh_all()

    def edit_client(item):
        selected_client = client_tree.item(item, 'values')
        client_id_entry.delete(0, tk.END)
        client_id_entry.insert(0, selected_client[0])
        client_name_entry.delete(0, tk.END)
        client_name_entry.insert(0, selected_client[1])
        client_contact_entry.delete(0, tk.END)
        client_contact_entry.insert(0, selected_client[2])

    ttk.Button(tab, text="Add Client", command=add_client_button, style='TButton').grid(column=0, row=3, padx=10, pady=10)
    ttk.Button(tab, text="Update Client", command=update_client_button, style='TButton').grid(column=1, row=3, padx=10, pady=10)
    ttk.Button(tab, text="Delete Client", command=delete_client_button, style='Red.TButton').grid(column=2, row=3, padx=10, pady=10)

    client_tree = ttk.Treeview(tab, columns=("idcli", "nom", "contact"), show='headings')
    client_tree.heading("idcli", text="Client ID")
    client_tree.heading("nom", text="Name")
    client_tree.heading("contact", text="Contact")
    client_tree.grid(column=0, row=4, columnspan=3, padx=10, pady=10, sticky='nsew')

    client_tree.column("idcli", anchor='center')
    client_tree.column("nom", anchor='center')
    client_tree.column("contact", anchor='center')

    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(4, weight=1)

    refresh_client_list()

    client_tree.bind("<Double-1>", lambda e: edit_client(client_tree.selection()[0]))

def create_car_tab(tab):
    global car_tree
    ttk.Label(tab, text="Car ID:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
    car_id_entry = ttk.Entry(tab)
    car_id_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Design:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
    car_design_entry = ttk.Entry(tab)
    car_design_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Price(Ar):").grid(column=0, row=2, padx=10, pady=10, sticky='w')
    car_price_entry = ttk.Entry(tab)
    car_price_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Quantity:").grid(column=0, row=3, padx=10, pady=10, sticky='w')
    car_quantity_entry = ttk.Entry(tab)
    car_quantity_entry.grid(column=1, row=3, padx=10, pady=10, sticky='ew')

    def add_car_button():
        cars = get_cars()
        car_ids = [car[0] for car in cars]
        car_designs = [car[1] for car in cars]

        if not (car_id_entry.get() and car_design_entry.get() and car_price_entry.get() and car_quantity_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_name(car_design_entry.get()):
            messagebox.showwarning("Warning", "Le design doit être uniquement composé de lettres")
            return
        if not validate_quantity(car_quantity_entry.get()):
            messagebox.showwarning("Warning", "La quantité doit être uniquement composée de chiffres")
            return
        if not validate_price(car_price_entry.get()):
            messagebox.showwarning("Warning", "Le prix doit être uniquement composé de chiffres")
            return
        if car_id_entry.get() in car_ids:
            messagebox.showwarning("Warning", "L'ID de la voiture existe déjà")
            return
        if car_design_entry.get() in car_designs:
            messagebox.showwarning("Warning", "Le design de la voiture existe déjà")
            return
        result = add_car(car_id_entry.get(), car_design_entry.get(), car_price_entry.get(), car_quantity_entry.get())
        messagebox.showinfo("Info", result)
        refresh_all()
        clear_fields([car_id_entry, car_design_entry, car_price_entry, car_quantity_entry])
        refresh_car_combobox()

    def update_car_button():
        if not car_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        cars = get_cars()
        selected_item = car_tree.selection()[0]
        selected_car = car_tree.item(selected_item, 'values')
        car_ids = [car[0] for car in cars if car[0] != selected_car[0]]
        car_designs = [car[1] for car in cars if car[0] != selected_car[0]]

        if car_id_entry.get() != selected_car[0]:
            messagebox.showwarning("Warning", "L'ID de la voiture ne peut pas être modifié")
            car_id_entry.delete(0, tk.END)
            car_id_entry.insert(0, selected_car[0])
            return

        if not (car_id_entry.get() and car_design_entry.get() and car_price_entry.get() and car_quantity_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_name(car_design_entry.get()):
            messagebox.showwarning("Warning", "Le design doit être uniquement composé de lettres")
            return
        if not validate_quantity(car_quantity_entry.get()):
            messagebox.showwarning("Warning", "La quantité doit être uniquement composée de chiffres")
            return
        if not validate_price(car_price_entry.get()):
            messagebox.showwarning("Warning", "Le prix doit être uniquement composé de chiffres")
            return
        if car_design_entry.get() in car_designs:
            messagebox.showwarning("Warning", "Le design de la voiture existe déjà")
            return
        result = update_car(car_id_entry.get(), car_design_entry.get(), car_price_entry.get(), car_quantity_entry.get())
        messagebox.showinfo("Info", result)
        refresh_all()
        clear_fields([car_id_entry, car_design_entry, car_price_entry, car_quantity_entry])

    def delete_car_button():
        if not car_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        selected_items = car_tree.selection()
        for selected_item in selected_items:
            selected_car = car_tree.item(selected_item, 'values')
            if any(purchase[2] == selected_car[0] for purchase in get_purchases()):
                messagebox.showwarning("Warning", "Veuillez d'abord supprimer les achats de cette voiture")
                return
            delete_car(selected_car[0])
        messagebox.showinfo("Info", "Voitures supprimées avec succès")
        refresh_all()

    def edit_car(item):
        selected_car = car_tree.item(item, 'values')
        car_id_entry.delete(0, tk.END)
        car_id_entry.insert(0, selected_car[0])
        car_design_entry.delete(0, tk.END)
        car_design_entry.insert(0, selected_car[1])
        car_price_entry.delete(0, tk.END)
        car_price_entry.insert(0, selected_car[2])
        car_quantity_entry.delete(0, tk.END)
        car_quantity_entry.insert(0, selected_car[3])

    ttk.Button(tab, text="Add Car", command=add_car_button, style='TButton').grid(column=0, row=4, padx=10, pady=10)
    ttk.Button(tab, text="Update Car", command=update_car_button, style='TButton').grid(column=1, row=4, padx=10, pady=10)
    ttk.Button(tab, text="Delete Car", command=delete_car_button, style='Red.TButton').grid(column=2, row=4, padx=10, pady=10)

    car_tree = ttk.Treeview(tab, columns=("idvoit", "design", "prix", "nombre"), show='headings')
    car_tree.heading("idvoit", text="Car ID")
    car_tree.heading("design", text="Design")
    car_tree.heading("prix", text="Price(Ar)")
    car_tree.heading("nombre", text="Quantity")
    car_tree.grid(column=0, row=5, columnspan=3, padx=10, pady=10, sticky='nsew')

    car_tree.column("idvoit", anchor='center')
    car_tree.column("design", anchor='center')
    car_tree.column("prix", anchor='center')
    car_tree.column("nombre", anchor='center')

    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(5, weight=1)

    refresh_car_list()

    car_tree.bind("<Double-1>", lambda e: edit_car(car_tree.selection()[0]))

def create_purchase_tab(tab):
    global purchase_tree, purchase_client_id_entry, purchase_car_id_entry

    ttk.Label(tab, text="Purchase Number:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
    purchase_num_entry = ttk.Entry(tab)
    purchase_num_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Client:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
    purchase_client_id_entry = ttk.Combobox(tab)
    purchase_client_id_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Car:").grid(column=0, row=2, padx=10, pady=10, sticky='w')
    purchase_car_id_entry = ttk.Combobox(tab)
    purchase_car_id_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Date:").grid(column=0, row=3, padx=10, pady=10, sticky='w')
    purchase_date_entry = DateEntry(tab)
    purchase_date_entry.grid(column=1, row=3, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="Quantity:").grid(column=0, row=4, padx=10, pady=10, sticky='w')
    purchase_quantity_entry = ttk.Entry(tab)
    purchase_quantity_entry.grid(column=1, row=4, padx=10, pady=10, sticky='ew')

    def add_purchase_button():
        purchases = get_purchases()
        purchase_ids = [purchase[0] for purchase in purchases]

        if not (purchase_num_entry.get() and purchase_client_id_entry.get() and purchase_car_id_entry.get() and purchase_quantity_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_purchase_num(purchase_num_entry.get()):
            messagebox.showwarning("Warning", "Le numéro d'achat doit être uniquement composé de chiffres")
            return
        if not validate_quantity(purchase_quantity_entry.get()):
            messagebox.showwarning("Warning", "La quantité doit être uniquement composée de chiffres")
            return
        if int(purchase_quantity_entry.get()) < 1:
            messagebox.showwarning("Warning", "Le nombre minimum d'achat est 1")
            return
        if purchase_num_entry.get() in purchase_ids:
            messagebox.showwarning("Warning", "L'ID de l'achat existe déjà")
            return
        design = purchase_car_id_entry.get()
        idvoit = next((car[0] for car in get_cars() if car[1] == design), None)
        if not idvoit:
            messagebox.showwarning("Warning", "Voiture non trouvée")
            return
        car_quantity = next(car[3] for car in get_cars() if car[0] == idvoit)
        if int(purchase_quantity_entry.get()) > car_quantity:
            messagebox.showwarning("Warning", "Stock de voiture insuffisant")
            return
        nom = purchase_client_id_entry.get()
        print("Client selected: ", nom)  # Debugging
        if nom not in [client[1] for client in get_clients()]:
            messagebox.showwarning("Warning", "Client non trouvé")
            return
        idcli = next(client[0] for client in get_clients() if client[1] == nom)
        result = add_purchase(purchase_num_entry.get(), idcli, idvoit, purchase_date_entry.get_date(), purchase_quantity_entry.get())
        messagebox.showinfo("Info", result)
        new_quantity = car_quantity - int(purchase_quantity_entry.get())
        update_car(idvoit, design, next(car[2] for car in get_cars() if car[0] == idvoit), new_quantity)
        add_revenue(int(purchase_quantity_entry.get()) * int(next(car[2] for car in get_cars() if car[0] == idvoit)))
        refresh_all()
        clear_fields([purchase_num_entry, purchase_client_id_entry, purchase_car_id_entry, purchase_quantity_entry])
        refresh_client_combobox()
        refresh_car_combobox()

    def update_purchase_button():
        if not purchase_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        if not (purchase_num_entry.get() and purchase_client_id_entry.get() and purchase_car_id_entry.get() and purchase_quantity_entry.get()):
            messagebox.showwarning("Warning", "Tous les champs doivent être remplis")
            return
        if not validate_purchase_num(purchase_num_entry.get()):
            messagebox.showwarning("Warning", "Le numéro d'achat doit être uniquement composé de chiffres")
            return
        if not validate_quantity(purchase_quantity_entry.get()):
            messagebox.showwarning("Warning", "La quantité doit être uniquement composée de chiffres")
            return
        selected_item = purchase_tree.selection()[0]
        selected_purchase = purchase_tree.item(selected_item, 'values')
        purchase_ids = [purchase[0] for purchase in get_purchases() if purchase[0] != selected_purchase[0]]

        if purchase_num_entry.get() != selected_purchase[0]:
            messagebox.showwarning("Warning", "L'ID de l'achat ne peut pas être modifié")
            purchase_num_entry.delete(0, tk.END)
            purchase_num_entry.insert(0, selected_purchase[0])
            return

        design = purchase_car_id_entry.get()
        idvoit = next((car[0] for car in get_cars() if car[1] == design), None)
        if not idvoit:
            messagebox.showwarning("Warning", "Voiture non trouvée")
            return
        car_quantity = next(car[3] for car in get_cars() if car[0] == idvoit)

        new_quantity = int(purchase_quantity_entry.get())
        old_quantity = int(selected_purchase[4])

        if new_quantity > car_quantity + old_quantity:
            messagebox.showwarning("Warning", "Stock de voiture insuffisant")
            return

        nom = purchase_client_id_entry.get()
        print("Client selected: ", nom)  # Debugging
        if nom not in [client[1] for client in get_clients()]:
            messagebox.showwarning("Warning", "Client non trouvé")
            return
        idcli = next(client[0] for client in get_clients() if client[1] == nom)

        result = update_purchase(purchase_num_entry.get(), idcli, idvoit, purchase_date_entry.get_date(), new_quantity)
        messagebox.showinfo("Info", result)

        updated_quantity = car_quantity + old_quantity - new_quantity
        update_car(idvoit, design, next(car[2] for car in get_cars() if car[0] == idvoit), updated_quantity)

        refresh_all()
        clear_fields([purchase_num_entry, purchase_client_id_entry, purchase_car_id_entry, purchase_quantity_entry])

    def delete_purchase_button():
        if not purchase_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        selected_items = purchase_tree.selection()
        for selected_item in selected_items:
            selected_purchase = purchase_tree.item(selected_item, 'values')
            idvoit = next((car[0] for car in get_cars() if car[1] == selected_purchase[2]), None)
            car_quantity = next(car[3] for car in get_cars() if car[0] == idvoit)
            new_quantity = car_quantity + int(selected_purchase[4])
            update_car(idvoit, selected_purchase[2], next(car[2] for car in get_cars() if car[0] == idvoit), new_quantity)
            delete_purchase(selected_purchase[0])
        messagebox.showinfo("Info", "Achats supprimés avec succès")
        refresh_all()

    def generate_invoice_button():
        if not purchase_tree.selection():
            messagebox.showwarning("Warning", "Veuillez sélectionner une liste")
            return
        selected_item = purchase_tree.selection()[0]
        selected_purchase = purchase_tree.item(selected_item, 'values')
        num_achat = selected_purchase[0]
        invoice_path = generate_invoice(num_achat)
        messagebox.showinfo("Info", f"Invoice generated: {invoice_path}")
        # Display the invoice directly
        webbrowser.open(f"file://{os.path.abspath(invoice_path)}")

    def edit_purchase(item):
        selected_purchase = purchase_tree.item(item, 'values')
        purchase_num_entry.delete(0, tk.END)
        purchase_num_entry.insert(0, selected_purchase[0])
        purchase_client_id_entry.set(selected_purchase[1])
        purchase_car_id_entry.set(selected_purchase[2])
        purchase_date_entry.set_date(selected_purchase[3])
        purchase_quantity_entry.delete(0, tk.END)
        purchase_quantity_entry.insert(0, selected_purchase[4])

    ttk.Button(tab, text="Add Purchase", command=add_purchase_button, style='TButton').grid(column=0, row=5, padx=10, pady=10)
    ttk.Button(tab, text="Update Purchase", command=update_purchase_button, style='TButton').grid(column=1, row=5, padx=10, pady=10)
    ttk.Button(tab, text="Delete Purchase", command=delete_purchase_button, style='Red.TButton').grid(column=2, row=5, padx=10, pady=10)
    ttk.Button(tab, text="Generate Invoice", command=generate_invoice_button, style='TButton').grid(column=0, row=6, padx=10, pady=10, columnspan=3)

    purchase_tree = ttk.Treeview(tab, columns=("numAchat", "clientName", "carDesign", "date", "qte"), show='headings')
    purchase_tree.heading("numAchat", text="Purchase Number")
    purchase_tree.heading("clientName", text="Client Name")
    purchase_tree.heading("carDesign", text="Car Design")
    purchase_tree.heading("date", text="Date")
    purchase_tree.heading("qte", text="Quantity")
    purchase_tree.grid(column=0, row=7, columnspan=3, padx=10, pady=10, sticky='nsew')

    purchase_tree.column("numAchat", anchor='center')
    purchase_tree.column("clientName", anchor='center')
    purchase_tree.column("carDesign", anchor='center')
    purchase_tree.column("date", anchor='center')
    purchase_tree.column("qte", anchor='center')

    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(7, weight=1)

    refresh_purchase_list()

    purchase_tree.bind("<Double-1>", lambda e: edit_purchase(purchase_tree.selection()[0]))

def create_reports_tab(tab):
    ttk.Label(tab, text="Start Date:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
    start_date_entry = DateEntry(tab)
    start_date_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

    ttk.Label(tab, text="End Date:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
    end_date_entry = DateEntry(tab)
    end_date_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

    def search_purchases_button():
        purchases = search_purchases(start_date_entry.get_date(), end_date_entry.get_date())
        for row in report_tree.get_children():
            report_tree.delete(row)
        for purchase in purchases:
            nom = get_client_name(purchase[1])
            design = get_car_design(purchase[2])
            report_tree.insert("", "end", values=(purchase[0], nom, design, purchase[3], purchase[4]))

    ttk.Button(tab, text="Search Purchases", command=search_purchases_button, style='TButton').grid(column=0, row=2, padx=10, pady=10, columnspan=2)

    def display_revenue():
        revenues = calculate_monthly_revenue()
        revenue_text = "\n".join([f"{month}: {revenue}" for month, revenue in revenues])
        messagebox.showinfo("Monthly Revenue", revenue_text)

    ttk.Button(tab, text="Show Revenue", command=display_revenue, style='TButton').grid(column=1, row=3, padx=10, pady=10)

    report_tree = ttk.Treeview(tab, columns=("numAchat", "clientName", "carDesign", "date", "qte"), show='headings')
    report_tree.heading("numAchat", text="Purchase Number")
    report_tree.heading("clientName", text="Client Name")
    report_tree.heading("carDesign", text="Car Design")
    report_tree.heading("date", text="Date")
    report_tree.heading("qte", text="Quantity")
    report_tree.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

    report_tree.column("numAchat", anchor='center')
    report_tree.column("clientName", anchor='center')
    report_tree.column("carDesign", anchor='center')
    report_tree.column("date", anchor='center')
    report_tree.column("qte", anchor='center')

    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(4, weight=1)

create_main_window()
