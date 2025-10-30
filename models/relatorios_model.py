from db.db_connection import conectar

class RelatoriosModel:
    @staticmethod
    def obter_resumo_geral():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_equipamentos FROM equipamento")
        total_equipamentos = cursor.fetchone()["total_equipamentos"]

        cursor.execute("SELECT COUNT(*) AS total_inventario FROM inventario")
        total_inventario = cursor.fetchone()["total_inventario"]

        cursor.execute("SELECT COUNT(*) AS total_consumos FROM consumo")
        total_consumos = cursor.fetchone()["total_consumos"]

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
    def listar_todos():
        
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                e.nome AS equipamento,
                i.setor AS setor,
                e.potencia_watts AS potencia,
                c.consumo_mensal_kwh AS consumo_kwh,
                c.custo_mensal AS custo,
                COALESCE(
                    comp.economia_reais, 
                    ROUND(
                        (comp.consumo_atual_kwh - comp.consumo_futuro_kwh)
                        * (c.custo_mensal / NULLIF(c.consumo_mensal_kwh, 0)),
                        2
                    ),
                    0
                ) AS economia
            FROM consumo c
            JOIN equipamento e ON c.id_equipamento = e.id_equipamento
            LEFT JOIN inventario i ON i.id_equipamento = e.id_equipamento
            LEFT JOIN consumos_has_comparativos ch ON ch.id_consumo = c.id_consumo
            LEFT JOIN comparativo comp ON comp.id_comparativo = ch.id_comparativo
            ORDER BY e.nome
        """)
        tabela = cursor.fetchall()
        conn.close()

        resumo = RelatoriosModel.obter_resumo_geral()

        return {
            "equipamentos": resumo["total_equipamentos"],
            "inventario": resumo["total_inventario"],
            "consumo": resumo["total_consumos"],
            "economia_total": resumo["total_economia"],
            "tabela": tabela
        }