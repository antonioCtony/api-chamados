import mysql.connector

def conexao ():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "nova senhas",
        database = "CHAMADOS",
        port=3306
    )


#