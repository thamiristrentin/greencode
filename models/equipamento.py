from db_connection import conectar

class EquipamentoModel:
    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Equipamento")
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados

    @staticmethod
    def adicionar(nome, quantidade, potencia, horas):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Equipamento (nome, quantidade, potencia_watts, horas_uso_diario)
            VALUES (%s, %s, %s, %s)
        """, (nome, quantidade, potencia, horas))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def deletar(id_equipamento):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Equipamento WHERE id_equipamento = %s", (id_equipamento,))
        conn.commit()
        cursor.close()
        conn.close()