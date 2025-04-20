from  flask import Flask, request, jsonify
from simulador import criar_chamado
import datetime

app= Flask(__name__)
@app.route("/Controle", methods=["POST"])

def receber():
    dados = request.get_json()
    id_cliente = dados.get("id_cliente")
    motivo = dados.get("Motivo","Transferencia de atendimento").capitalize()

    #verficação de id
    if not id_cliente:
        return jsonify({"Erro": "ID_cliente é obrigatorio"}),400
 
    #Chama função para criar o chamado
    resultado = criar_chamado(id_cliente, motivo)
    return jsonify({"Mensagem":resultado})
        

if __name__ == "__main__":
    app.run(debug =True)