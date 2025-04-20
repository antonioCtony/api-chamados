import time;
import random;
from flask import Flask; 

lista_chamados = []

#Simulando uma função para criar o chamado:
def criar_chamado(id_cliente, motivo):
    numero = random.randrange(1000,9999) #Gera chamados aleatorio

    for chamado in lista_chamados: #Verifica se já tem um chamado aberto para o cliente no momento da transferencia
        if chamado["Cliente"] == id_cliente  and chamado["Status"] == "Aberto":
            return f"Chamado já esta aberto {id_cliente}, Número: {chamado['Numero']} "

    chamado = {
        "Cliente" : id_cliente,
        "Motivo" : motivo,
        "Status" : "Aberto",
        "Numero" : numero
    }
    lista_chamados.append(chamado)
    return f"novo chamado criado: {chamado}, Número {chamado['Numero']}"
    

def fluxo_atendimetno(): #Simulando o fluxo de atendimento;
    cliente = "13215"

    print(f"Bot abriu o chamado para: {cliente}")
    print(criar_chamado(cliente, "Primeiro contato no chat"))

    time.sleep(2) #espera por dois segundos 
    
    #Fechando o chamado manualmente
    for chamado in lista_chamados:
        if chamado["Cliente"] == cliente:
            chamado["Status"] = "Fechado"
            print(f"Chamado foi fechado {chamado['Numero']}")
    
    time.sleep(2)

    print("Gerente transferido para outro chat...")
    print(criar_chamado(cliente,"Transferencia de atendimento"))
fluxo_atendimetno()

