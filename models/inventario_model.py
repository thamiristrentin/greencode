from db.db_connection import conectar

class InventarioModel:
    @staticmethod
    def listar_todos():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.id_inventario, i.nome, i.marca, i.descricao, i.setor, i.valor,
                e.nome AS equipamento
            FROM inventario i
            JOIN equipamento e ON i.id_equipamento = e.id_equipamento
        """)
        dados = cursor.fetchall()
        conn.close()
        return dados

    @staticmethod
    def inserir(nome, marca, descricao, setor, valor, id_equipamento):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventario (nome, marca, descricao, setor, valor, id_equipamento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, marca, descricao, setor, valor, id_equipamento))
        conn.commit()
        conn.close()
