import os
import requests
import json
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
TOKEN = os.getenv('TRELLO_TOKEN')

if not API_KEY or not TOKEN:
    print("❌ Erro: As variáveis TRELLO_API_KEY e TRELLO_TOKEN devem estar configuradas no ambiente (ou no arquivo .env).")
    exit(1)

BASE_URL = 'https://api.trello.com/1'
AUTH = {'key': API_KEY, 'token': TOKEN}

def create_board(name):
    print(f"Criando quadro: {name}...")
    url = f"{BASE_URL}/boards/"
    payload = {
        **AUTH,
        'name': name,
        'defaultLists': 'false', # Evita criar as listas padrões do Trello (To Do, Doing, Done)
        'prefs_background': 'blue'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    board = response.json()
    print(f"✅ Quadro criado com sucesso! URL: {board.get('url')}")
    return board['id']

def create_list(board_id, name, pos='bottom'):
    print(f"Criando lista: {name}...")
    url = f"{BASE_URL}/lists"
    payload = {
        **AUTH,
        'name': name,
        'idBoard': board_id,
        'pos': pos
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['id']

def create_label(board_id, name, color):
    print(f"Criando etiqueta: {name} ({color})...")
    url = f"{BASE_URL}/labels"
    payload = {
        **AUTH,
        'name': name,
        'color': color,
        'idBoard': board_id
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['id']

def create_card(list_id, name):
    print(f"Criando cartão: {name}...")
    url = f"{BASE_URL}/cards"
    payload = {
        **AUTH,
        'idList': list_id,
        'name': name,
        'pos': 'bottom'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['id']

def main():
    try:
        # 1. Cria o Quadro
        board_name = "QA & Automation Portfolio"
        board_id = create_board(board_name)

        # 2. Cria as Listas na ordem exata
        lists = ["Backlog", "Test Design", "In Progress", "CI/CD Execution", "Done", "Bugs"]
        list_ids = {}
        for lst in lists:
            list_ids[lst] = create_list(board_id, lst)

        # 3. Cria as Etiquetas Padrão
        labels = [
            {"name": "UI Test", "color": "blue"},
            {"name": "API Test", "color": "green"},
            {"name": "E2E", "color": "purple"},
            {"name": "Bug", "color": "red"},
            {"name": "CI/CD", "color": "black"}
        ]
        for lbl in labels:
            create_label(board_id, lbl['name'], lbl['color'])

        # 4. Cria 3 Cartões de Exemplo no Backlog
        backlog_id = list_ids["Backlog"]
        sample_cards = [
            "Implement Login E2E Tests",
            "Configure GitHub Actions Pipeline",
            "Setup Datadog Integration"
        ]
        for card in sample_cards:
            create_card(backlog_id, card)

        print("\n🎉 Setup do Quadro de QA concluído com sucesso!")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro durante a comunicação com a API do Trello: {e}")
        if e.response is not None:
            print(f"Detalhes: {e.response.text}")
        exit(1)

if __name__ == '__main__':
    main()
