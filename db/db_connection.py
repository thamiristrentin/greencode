import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="maglev.proxy.rlwy.net",
        port=25116,
        user="root",
        password="tstSBXUgVdJcECuNRvHyOySnItSpyUXA",
        database="greencode",
        charset="utf8mb4"
    )
