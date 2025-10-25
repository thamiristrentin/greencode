from db.db_connection import conectar

class TarifaModel:
    @staticmethod
    def listar_todas():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarifa")
        dados = cursor.fetchall()
        conn.close()
        return dados
