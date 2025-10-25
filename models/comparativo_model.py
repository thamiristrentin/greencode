from db.db_connection import conectar

class ComparativoModel:
    @staticmethod
    def listar_todos():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comparativo")
        dados = cursor.fetchall()
        conn.close()
        return dados
