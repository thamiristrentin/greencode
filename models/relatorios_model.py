from db.db_connection import conectar

class RelatoriosModel:
    @staticmethod
    def resumo_consumo():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.nome AS equipamento,
                   SUM(c.consumo_mensal_kwh) AS consumo_total,
                   SUM(c.custo_mensal) AS custo_total
            FROM Consumo c
            JOIN Equipamento e ON c.id_equipamento = e.id_equipamento
            GROUP BY e.nome
            ORDER BY consumo_total DESC
        """)
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

    @staticmethod
    def economia_total():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT SUM(economia_kwh) AS total_kwh,
                   SUM(economia_reais) AS total_reais
            FROM Comparativo
        """)
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado