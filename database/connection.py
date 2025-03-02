import sqlite3

class DatabaseConnection:
    def __init__(self, db_name=r"\\172.25.1.6\publicas\mjaristizabal\db.sqlite3"):
        """Inicializa la conexión a la base de datos."""
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Establece la conexión con SQLite y la devuelve."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            print("✅ Conexión a la base de datos establecida correctamente.")
            return self.conn
        except sqlite3.Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("🔌 Conexión a la base de datos cerrada.")

# Ejemplo de uso
if __name__ == "__main__":
    db = DatabaseConnection()
    conn = db.connect()
    if conn:
        db.close()