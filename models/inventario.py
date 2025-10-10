from db_connection import conectar

class InventarioModel:
    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, e.nome AS equipamento
            FROM Inventario i
            JOIN Equipamento e ON i.id_equipamento = e.id_equipamento
        """)
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

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