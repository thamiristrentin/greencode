from db.db_connection import conectar

class EquipamentoModel:
    @staticmethod
    def listar_todos():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipamento")
        dados = cursor.fetchall()
        conn.close()
        return dados

    @staticmethod
    def inserir(nome, quantidade, potencia_watts, horas_uso_diario):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO equipamento (nome, quantidade, potencia_watts, horas_uso_diario)
            VALUES (%s, %s, %s, %s)
        """, (nome, quantidade, potencia_watts, horas_uso_diario))
        conn.commit()
        conn.close()
