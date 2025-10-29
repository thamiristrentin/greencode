# models/relatorios.py
from db.db_connection import conectar

class RelatoriosModel:
    @staticmethod
    def obter_resumo_geral():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Total de equipamentos
        cursor.execute("SELECT COUNT(*) AS total_equipamentos FROM equipamento")
        total_equipamentos = cursor.fetchone()["total_equipamentos"]

        # Total de itens de inventário
        cursor.execute("SELECT COUNT(*) AS total_inventario FROM inventario")
        total_inventario = cursor.fetchone()["total_inventario"]

        # Total de registros de consumo
        cursor.execute("SELECT COUNT(*) AS total_consumos FROM consumo")
        total_consumos = cursor.fetchone()["total_consumos"]

        # Economia total (soma em reais)
        cursor.execute("SELECT COALESCE(SUM(economia_reais), 0) AS total_economia FROM comparativo")
        total_economia = cursor.fetchone()["total_economia"]

        conn.close()

        return {
            "total_equipamentos": total_equipamentos,
            "total_inventario": total_inventario,
            "total_consumos": total_consumos,
            "total_economia": total_economia
        }

    @staticmethod
    def listar_detalhado():
        """
        Retorna uma lista de visão geral combinando dados de todas as tabelas.
        Ideal para exportar relatórios completos (PDF/Excel).
        """
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                e.nome AS equipamento,
                e.quantidade,
                e.potencia_watts,
                e.horas_uso_diario,
                i.setor,
                t.valor_kwh,
                c.consumo_mensal_kwh,
                c.custo_mensal,
                comp.economia_kwh,
                comp.economia_reais
            FROM consumo c
            JOIN equipamento e ON c.id_equipamento = e.id_equipamento
            JOIN tarifa t ON c.id_tarifa = t.id_tarifa
            LEFT JOIN inventario i ON i.id_equipamento = e.id_equipamento
            LEFT JOIN consumos_has_comparativos ch ON ch.id_consumo = c.id_consumo
            LEFT JOIN comparativo comp ON comp.id_comparativo = ch.id_comparativo
            ORDER BY e.nome
        """)
        dados = cursor.fetchall()
        conn.close()
        return dados
