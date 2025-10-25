import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="",  # substitui se o host for outro
        port=,  # confirma no painel Railway
        user="",  # ou o usuário do teu banco
        password="",
        database="",
        charset="utf8mb4"
    )
