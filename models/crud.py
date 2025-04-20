import random
from flask import Flask, request, jsonify
from msqly import conexao 

app = Flask(__name__)

def get_db_cursor():
    conexao = conexao()
    return conexao.cursor(), conexao

# Rota para criar uma nova tarefa (agora no banco de dados)
@app.route("/tasks", methods=["POST"])
def criar_task():
    data = request.get_json()

    #Verfica se os dados necessários foram fornecidos
    if not all(k in data for k in ["id_cliente","id_atendente","data_inicio","data_fim","hora_inicio","hora_fim","estado"
    ,"problema","descricao"]):
        return jsonify({"message": "Dados faltando, certifique de forncer todos os campos"}), 400
    cursor, conexao = get_db_cursor

    # Gerar um número de chamado aleatório
    numero_chamado = random.randint(1000, 9999)

    # SQL para inserir dados no banco
    sql = """
        INSERT INTO tasks (id_cliente, id_atendente, numero_chamado, data_inicio, data_fim, hora_inicio, hora_fim, estado, problema, descricao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Valores que serão inseridos
    valores = (
        data.get("id_cliente"),
        data.get("id_atendente"),
        numero_chamado,
        data.get("data_inicio"),
        data.get("data_fim"),
        data.get("hora_inicio"),
        data.get("hora_fim"),
        data.get("estado"),
        data.get("problema"),
        data.get("descricao")
    )
     # Executando o comando SQL
    try:
        cursor.execute(sql, valores)
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        return jsonify({"Messege":f"Erro ao criar tarefa: {str(e)}"}),500
    finally:
        cursor.close()
        conexao.close()


    return jsonify({
        "message": "Tarefa criada com sucesso!",
        "task": {
            "id_cliente": data.get("id_cliente"),
            "id_atendente": data.get("id_atendente"),
            "numero_chamado": numero_chamado,
            "data_inicio": data.get("data_inicio"),
            "data_fim": data.get("data_fim"),
            "hora_inicio": data.get("hora_inicio"),
            "hora_fim": data.get("hora_fim"),
            "estado": data.get("estado"),
            "problema": data.get("problema"),
            "descricao": data.get("descricao")
        }
    }), 201

# Rota para listar todas as tarefas
@app.route("/tasks", methods=["GET"])
def lista_tasks():
    conexao= conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()  # Retorna todos os registros da tabela

    cursor.close()
    conexao.close()

    # Formatar os resultados antes de retornar
    result = []
    for task in tasks:
        result.append({
            "id": task[0],
            "id_cliente": task[1],
            "id_atendente": task[2],
            "numero_chamado": task[3],
            "data_inicio": task[4],
            "data_fim": task[5],
            "hora_inicio": task[6],
            "hora_fim": task[7],
            "estado": task[8],
            "problema": task[9],
            "descricao": task[10]
        })

    return jsonify({
        "tasks": result,
        "total": len(result)
    })

# Rota para buscar uma tarefa específica pelo ID
@app.route("/tasks/<int:task_id>", methods=["GET"])
def obter_task(task_id):
    conexao= conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not task:
        return jsonify({"message": "Tarefa não encontrada."}), 404

    return jsonify({
        "id": task[0],
        "id_cliente": task[1],
        "id_atendente": task[2],
        "numero_chamado": task[3],
        "data_inicio": task[4],
        "data_fim": task[5],
        "hora_inicio": task[6],
        "hora_fim": task[7],
        "estado": task[8],
        "problema": task[9],
        "descricao": task[10]
    })

# Rota para atualizar uma tarefa existente
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def atualizar_task(task_id):
    data = request.get_json()

    conexao = conexao()
    cursor = conexao.cursor()

    # SQL para atualizar dados no banco
    sql = """
        UPDATE tasks
        SET id_cliente = %s, id_atendente = %s, data_inicio = %s, data_fim = %s, hora_inicio = %s, hora_fim = %s, estado = %s, problema = %s, descricao = %s
        WHERE id = %s
    """
    valores = (
        data.get("id_cliente"),
        data.get("id_atendente"),
        data.get("data_inicio"),
        data.get("data_fim"),
        data.get("hora_inicio"),
        data.get("hora_fim"),
        data.get("estado"),
        data.get("problema"),
        data.get("descricao"),
        task_id
    )
    try:
        cursor.execute(sql, valores)
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        return jsonify({"message":f"Erro ao atualizar tarefa{str(e)}"}),500
    finally:
        cursor.close()
        conexao.close()
    
    return jsonify({"Message": "Tarefa atualizada com sucesso!"})

# Rota para deletar uma tarefa
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def deletar_task(task_id):
    conexao= conexao()
    cursor = conexao.cursor()

    # SQL para deletar a tarefa
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({"message": "Tarefa deletada com sucesso!"})

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
