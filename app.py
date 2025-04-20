
from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = [] #lista para armazenar tarefas
tasks_id_control = 1 #Controlar de ID, para garantir unicidade 

app = Flask(__name__)
@app.route("/tasks", methods =["POST"])

def criar_tasks():
    global tasks_id_control
    data = request.get_json() #Pega os dados que estão sendo enviados na requisição
    nova_task = {
        "id" : tasks_id_control,
        "titulo": data.get("titulo"), #Pega o titulo enviado
        "descricao" : data.get("descricao"),
        "completo" : False #tarefa começa como incompleta
    }
    tasks.append(nova_task) #adiciona uma nova tarefa na lista
    tasks_id_control += 1 #incrementa toda vez que uma nova task for criada
    return jsonify({"Message": "Tarefa criada com sucesso!","task": nova_task}),201


@app.route("/tasks", methods=["GET"])
def lista_task():
    return jsonify({"taks":tasks, "total": len(tasks)})

@app.route("/task/<int:task_id>", methods=["GET"])
def lista_tasks(task_id):
    #Procura a tarefa por id
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"Message": "Tarefa não foi encontrada."}),404
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods =(["PUT"]))
def update_tasks():
    task = next((t for t in tasks if t["id"]))

if __name__ == "__main__":
    app.run(debug=True)