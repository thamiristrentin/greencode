from db_connection import conectar

class TarifaModel:
    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Tarifa ORDER BY vigencia_inicio DESC")
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

    @staticmethod
    def adicionar(valor_kwh, inicio, fim):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Tarifa (valor_kwh, vigencia_inicio, vigencia_fim)
            VALUES (%s, %s, %s)
        """, (valor_kwh, inicio, fim))
        conn.commit()
        cursor.close()
        conn.close()
