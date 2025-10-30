import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="maglev.proxy.rlwy.net",  # substitui se o host for outro
        port=25116,  # confirma no painel Railway
        user="root",  # ou o usuário do teu banco
        password="tstSBXUgVdJcECuNRvHyOySnItSpyUXA",
        database="greencode",
        charset="utf8mb4"
    )
