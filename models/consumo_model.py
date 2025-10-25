from db.db_connection import conectar

class ConsumoModel:
    @staticmethod
    def listar_todos():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id_consumo, e.nome AS equipamento, t.valor_kwh, 
                c.consumo_diario_kwh, c.consumo_mensal_kwh, 
                c.custo_diario, c.custo_mensal
            FROM consumo c
            JOIN equipamento e ON c.id_equipamento = e.id_equipamento
            JOIN tarifa t ON c.id_tarifa = t.id_tarifa
        """)
        dados = cursor.fetchall()
        conn.close()
        return dados
