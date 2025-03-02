from database.connection import DatabaseConnection

db = DatabaseConnection()
conn = db.connect()

if conn:
    print("Conexión establecida.")

# db.close()