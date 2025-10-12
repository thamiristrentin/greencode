from db.db_connection import conectar

class ComparativoModel:
    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Comparativo ORDER BY id_comparativo DESC")
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

    @staticmethod
    def adicionar(descricao, atual, futuro):
        economia_kwh = round(atual - futuro, 2)
        economia_reais = round(economia_kwh * 1.02, 2)  # valor estimado com tarifa média
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Comparativo (descricao, consumo_atual_kwh, consumo_futuro_kwh, economia_kwh, economia_reais)
            VALUES (%s, %s, %s, %s, %s)
        """, (descricao, atual, futuro, economia_kwh, economia_reais))
        conn.commit()
        cursor.close()
        conn.close()