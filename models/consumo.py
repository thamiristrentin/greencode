from db_connection import conectar

class ConsumoModel:
    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, e.nome AS equipamento, t.valor_kwh
            FROM Consumo c
            JOIN Equipamento e ON c.id_equipamento = e.id_equipamento
            JOIN Tarifa t ON c.id_tarifa = t.id_tarifa
        """)
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

    @staticmethod
    def calcular_consumo(id_equipamento, id_tarifa):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.quantidade, e.potencia_watts, e.horas_uso_diario, t.valor_kwh
            FROM Equipamento e
            JOIN Tarifa t ON t.id_tarifa = %s
            WHERE e.id_equipamento = %s
        """, (id_tarifa, id_equipamento))
        dados = cursor.fetchone()
        cursor.close()
        conn.close()

        if not dados:
            return None

        consumo_diario = (dados['potencia_watts'] * dados['horas_uso_diario'] * dados['quantidade']) / 1000
        consumo_mensal = consumo_diario * 30
        custo_diario = consumo_diario * dados['valor_kwh']
        custo_mensal = consumo_mensal * dados['valor_kwh']

        return (round(consumo_diario, 2), round(consumo_mensal, 2), round(custo_diario, 2), round(custo_mensal, 2))

    @staticmethod
    def adicionar(id_equipamento, id_tarifa, data_calculo, consumo_diario, consumo_mensal, custo_diario, custo_mensal):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Consumo (id_equipamento, id_tarifa, data_calculo, consumo_diario_kwh, consumo_mensal_kwh, custo_diario, custo_mensal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_equipamento, id_tarifa, data_calculo, consumo_diario, consumo_mensal, custo_diario, custo_mensal))
        conn.commit()
        cursor.close()
        conn.close()
