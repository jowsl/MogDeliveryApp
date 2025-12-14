import requests 
import time
import json
import signal

discord_url = "https://discord.com/api/webhooks/1449506737592729724/oX58eCUnUfEV02wPxobZP-SGj3w7wD68EO1lopyQsD8j9laciJzmolpoVe4L8_9oLkKq"

def timeout_adicionar_item(signum, frame):
    raise TimeoutError

signal.signal(signal.SIGALRM, timeout_adicionar_item)


def salvar(lista_de_itens):
    path = "itens.txt"
    with open(path, "w", encoding="utf-8") as arq:
        json.dump(lista_de_itens, arq, ensure_ascii=False, indent=4)
        print("Novo item adicionado ")

def carregar():
    path="itens.txt"
    try:
        with open(path, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    


def enviar_alerta(nome_item, preco, mundo, item_id):
    mensagem_texto = f"\n🚨 **ALERTA DE PREÇO!** 🚨\n\n<@113329355618258944>, o item **{nome_item}** está custando **{preco:,} **!\n 🌎: **{mundo}**\nhttps://universalis.app/market/{item_id}"
    
    dados = {
        "content": mensagem_texto
    }
    
    try:
        requests.post(discord_url, json=dados)
        print("-> Notificação enviada para o Discord!")
    except Exception as e:
        print(f"-> Falha ao enviar para o Discord: {e}")

def enviar_preco_alto(msg):

    dados = {
        "content": msg
    }
    
    try:
        requests.post(discord_url, json=dados)
        print("-> Notificação enviada para o Discord!")
    except Exception as e:
        print(f"-> Falha ao enviar para o Discord: {e}")


def priceVerifier(item, flag):

    try:

        headers = {
            'User-Agent': 'ProjectPriceNotifier/1.0'
        }

        url = f"https://universalis.app/api/v2/Crystal/{item['id']}"
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if not data.get('listings'): return print("Ninguém vendendo esse item.")     

            melhor_valor = data['listings'][0]

            preco_atual = melhor_valor['pricePerUnit']
            mundo = melhor_valor['worldName']

            if preco_atual <= item['max']:
                return {
                    "preco": preco_atual,
                    "mundo": mundo
                }
            elif preco_atual > melhor_valor['pricePerUnit'] and flag == 1:
                msg = f"\n Preço ainda **alto** :troll:\n\tMelhor: {preco_atual}\n\tMundo: {mundo}"
                enviar_preco_alto(msg)
        else:
            print(f"Erro na API - {response.status_code}")

    except Exception as e:
        print(f"Problema de conexão {e}")
    
    return None

    
#main
def main():

    lista_de_itens = []

    lista_de_itens = carregar()

    if lista_de_itens == []: return 1

    print(lista_de_itens)

    while True:

        for item in lista_de_itens:
            resultado = priceVerifier(item, 0)

            if resultado: enviar_alerta(item['nome'], resultado['preco'], resultado['mundo'], item['id'])
        
            time.sleep(5)


        add_item = None
        signal.alarm(30)
        try:
            add_item = input("Enter para adicionar outro item.")
        
            if add_item != None:

                signal.alarm(0)         
                id = input("Qual o ID: ")
                preco_max = int(input("Valor máximo: "))
                nome = input("Qual o nome: ")
                lista_de_itens.append(
                    {"id": id, "max": preco_max, "nome": nome}
                )
                resultado = priceVerifier(item, 1)
                salvar(lista_de_itens)
                continue

        except TimeoutError:
            print(">> continuando, sleep por 570 seg")
            
        
        time.sleep(570)


if __name__ == "__main__":
    main()
