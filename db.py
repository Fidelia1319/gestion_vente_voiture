import mysql.connector
from mysql.connector import Error

def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='car_sales'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

def add_client(idcli, nom, contact):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO CLIENT (idcli, nom, contact) VALUES (%s, %s, %s)"
    cursor.execute(query, (idcli, nom, contact))
    connection.commit()
    cursor.close()
    connection.close()
    return "Client added successfully"

def get_clients():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CLIENT")
    clients = cursor.fetchall()
    cursor.close()
    connection.close()
    return clients

def update_client(idcli, nom, contact):
    connection = connect()
    cursor = connection.cursor()
    query = "UPDATE CLIENT SET nom = %s, contact = %s WHERE idcli = %s"
    cursor.execute(query, (nom, contact, idcli))
    connection.commit()
    cursor.close()
    connection.close()
    return "Client updated successfully"

def delete_client(idcli):
    connection = connect()
    cursor = connection.cursor()
    query = "DELETE FROM CLIENT WHERE idcli = %s"
    cursor.execute(query, (idcli,))
    connection.commit()
    cursor.close()
    connection.close()
    return "Client deleted successfully"

def add_car(idvoit, design, prix, nombre):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO VOITURE (idvoit, design, prix, nombre) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (idvoit, design, prix, nombre))
    connection.commit()
    cursor.close()
    connection.close()
    return "Car added successfully"

def get_cars():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM VOITURE")
    cars = cursor.fetchall()
    cursor.close()
    connection.close()
    return cars

def update_car(idvoit, design, prix, nombre):
    connection = connect()
    cursor = connection.cursor()
    query = "UPDATE VOITURE SET design = %s, prix = %s, nombre = %s WHERE idvoit = %s"
    cursor.execute(query, (design, prix, nombre, idvoit))
    connection.commit()
    cursor.close()
    connection.close()
    return "Car updated successfully"

def delete_car(idvoit):
    connection = connect()
    cursor = connection.cursor()
    query = "DELETE FROM VOITURE WHERE idvoit = %s"
    cursor.execute(query, (idvoit,))
    connection.commit()
    cursor.close()
    connection.close()
    return "Car deleted successfully"

def add_purchase(numAchat, idcli, idvoit, date, qte):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO ACHAT (numAchat, idcli, idvoit, date, qte) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (numAchat, idcli, idvoit, date, qte))
    connection.commit()
    cursor.close()
    connection.close()
    return "Purchase added successfully"

def get_purchases():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ACHAT")
    purchases = cursor.fetchall()
    cursor.close()
    connection.close()
    return purchases

def update_purchase(numAchat, idcli, idvoit, date, qte):
    connection = connect()
    cursor = connection.cursor()
    query = "UPDATE ACHAT SET idcli = %s, idvoit = %s, date = %s, qte = %s WHERE numAchat = %s"
    cursor.execute(query, (idcli, idvoit, date, qte, numAchat))
    connection.commit()
    cursor.close()
    connection.close()
    return "Purchase updated successfully"

def delete_purchase(numAchat):
    connection = connect()
    cursor = connection.cursor()
    query = "DELETE FROM ACHAT WHERE numAchat = %s"
    cursor.execute(query, (numAchat,))
    connection.commit()
    cursor.close()
    connection.close()
    return "Purchase deleted successfully"

def search_purchases(start_date, end_date):
    connection = connect()
    cursor = connection.cursor()
    query = "SELECT * FROM ACHAT WHERE date BETWEEN %s AND %s"
    cursor.execute(query, (start_date, end_date))
    purchases = cursor.fetchall()
    cursor.close()
    connection.close()
    return purchases

def calculate_monthly_revenue():
    connection = connect()
    cursor = connection.cursor()
    query = """
    SELECT DATE_FORMAT(date, '%Y-%m') as month, SUM(prix * qte)
    FROM ACHAT JOIN VOITURE ON ACHAT.idvoit = VOITURE.idvoit
    GROUP BY month
    ORDER BY month DESC
    LIMIT 6
    """
    cursor.execute(query)
    revenues = cursor.fetchall()
    cursor.close()
    connection.close()
    return revenues

def add_revenue(amount):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO revenue (amount) VALUES (%s)"
    cursor.execute(query, (amount,))
    connection.commit()
    cursor.close()
    connection.close()
