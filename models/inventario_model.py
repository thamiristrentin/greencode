from db.db_connection import conectar

class InventarioModel:
    def listar_todos(self):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.id_inventario, i.nome, i.marca, i.descricao, i.identificacao, i.setor, i.valor, i.id_equipamento, e.nome AS equipamento
            FROM Inventario i
            JOIN Equipamento e ON i.id_equipamento = e.id_equipamento
            ORDER BY i.id_inventario;
        """)
        resultado = cursor.fetchall()
        cursor.close()
        conexao.close()
        return resultado

    @staticmethod
    def adicionar(nome, marca, descricao, identificacao, setor, valor, id_equipamento):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Inventario (nome, marca, descricao, identificacao, setor, valor, id_equipamento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, marca, descricao, identificacao, setor, valor, id_equipamento))
        conn.commit()
        cursor.close()
        conn.close()