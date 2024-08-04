from fpdf import FPDF
import os
import datetime
from db import connect


class PDF(FPDF):
    def header(self):
        # Add logo
        self.image('logo.png', 10, 8, 33)  # You need a logo image named 'logo.png' in the same directory
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Car Sales Management System', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Invoice', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_invoice_section(self, title, data):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(5)
        self.set_font('Arial', '', 12)
        for label, value in data.items():
            self.cell(0, 10, f"{label}: {value}", 0, 1, 'L')
        self.ln(10)


def generate_invoice(numAchat):
    connection = connect()
    cursor = connection.cursor()
    query = """
        SELECT ACHAT.numAchat, CLIENT.nom, CLIENT.contact, VOITURE.design, ACHAT.date, ACHAT.qte, VOITURE.prix 
        FROM ACHAT
        JOIN CLIENT ON ACHAT.idcli = CLIENT.idcli
        JOIN VOITURE ON ACHAT.idvoit = VOITURE.idvoit
        WHERE ACHAT.numAchat = %s
    """
    cursor.execute(query, (numAchat,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    pdf = PDF()
    pdf.num_achat = numAchat
    pdf.add_page()

    pdf.set_fill_color(200, 220, 255)

    client_info = {
        "Purchase Number": result[0],
        "Client Name": result[1],
        "Contact": result[2]
    }
    car_info = {
        "Car Design": result[3],
        "Date": result[4],
        "Quantity": result[5],
        "Price per unit": f"Ar{result[6]:,.2f}",
        "Total": f"Ar{result[5] * result[6]:,.2f}"
    }

    pdf.add_invoice_section("Client Information", client_info)
    pdf.add_invoice_section("Car Information", car_info)

    # Adding a table for better formatting
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Description', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Quantity', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Unit Price', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Total Price', 1, 1, 'C', 1)

    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, result[3], 1)
    pdf.cell(30, 10, str(result[5]), 1)
    pdf.cell(40, 10, f"Ar{result[6]:,.2f}", 1)
    pdf.cell(40, 10, f"Ar{result[5] * result[6]:,.2f}", 1, 1)

    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Date: {datetime.date.today().strftime('%B %d, %Y')}", 0, 1, 'R')

    if not os.path.exists('invoices'):
        os.makedirs('invoices')

    pdf_path = os.path.join('invoices', f"Invoice_{numAchat}.pdf")
    pdf.output(pdf_path)

    return pdf_path
