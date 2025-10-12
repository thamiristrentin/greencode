import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="tramway.proxy.rlwy.net",  # substitui se o host for outro
        port=50168,  # confirma no painel Railway
        user="root",  # ou o usuário do teu banco
        password="VLywNlEIRkNZaxTPGWMhXSHWAabvPmGG",
        database="greencode",
        charset="utf8mb4"
    )