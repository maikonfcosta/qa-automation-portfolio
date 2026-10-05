import os
import requests

# 1. Carregar Variáveis de Ambiente
TRELLO_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.environ.get("TRELLO_BOARD_ID") # Ex: O2CfizDA (ID do quadro que criamos)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") # Fornecido automaticamente pelo GitHub Actions
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY") # Formato: usuario/repositorio

if not all([TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID, GITHUB_TOKEN, GITHUB_REPO]):
    print("❌ Faltam variáveis de ambiente. Verifique os Secrets do GitHub.")
    exit(1)

TRELLO_BASE_URL = "https://api.trello.com/1"
TRELLO_AUTH = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}

def get_bugs_list_id():
    """Busca o ID da lista 'Bugs' no quadro."""
    url = f"{TRELLO_BASE_URL}/boards/{TRELLO_BOARD_ID}/lists"
    resp = requests.get(url, params=TRELLO_AUTH)
    resp.raise_for_status()
    for lst in resp.json():
        if lst["name"].lower() == "bugs":
            return lst["id"]
    return None

def get_cards_in_list(list_id):
    """Retorna todos os cartões de uma lista."""
    url = f"{TRELLO_BASE_URL}/lists/{list_id}/cards"
    resp = requests.get(url, params=TRELLO_AUTH)
    resp.raise_for_status()
    return resp.json()

def has_github_issue_attached(card_id):
    """Verifica se o cartão já possui um anexo do GitHub."""
    url = f"{TRELLO_BASE_URL}/cards/{card_id}/attachments"
    resp = requests.get(url, params=TRELLO_AUTH)
    resp.raise_for_status()
    attachments = resp.json()
    for att in attachments:
        if "github.com" in att.get("url", "") and "/issues/" in att.get("url", ""):
            return True
    return False

def create_github_issue(title, description, trello_url):
    """Cria uma Issue no repositório do GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    body = description + f"\n\n---\n🔗 _Origem: [Cartão no Trello]({trello_url})_"
    payload = {"title": title, "body": body}
    
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["html_url"]

def attach_url_to_trello_card(card_id, url_to_attach):
    """Anexa a URL da nova Issue no cartão do Trello para não duplicar no futuro."""
    url = f"{TRELLO_BASE_URL}/cards/{card_id}/attachments"
    payload = {**TRELLO_AUTH, "url": url_to_attach, "name": "GitHub Issue"}
    resp = requests.post(url, data=payload)
    resp.raise_for_status()

def main():
    print(f"🔄 Iniciando sincronização Trello -> GitHub ({GITHUB_REPO})")
    
    bugs_list_id = get_bugs_list_id()
    if not bugs_list_id:
        print("❌ Lista 'Bugs' não encontrada no quadro Trello especificado.")
        exit(1)
        
    cards = get_cards_in_list(bugs_list_id)
    print(f"📋 Encontrados {len(cards)} cartões na lista de Bugs.")
    
    for card in cards:
        print(f"\nVerificando cartão: {card['name']}")
        
        if has_github_issue_attached(card['id']):
            print("✅ Este cartão já possui uma Issue no GitHub associada. Ignorando.")
            continue
            
        print("🚀 Criando nova Issue no GitHub...")
        issue_url = create_github_issue(card['name'], card.get('desc', ''), card['url'])
        print(f"✅ Issue criada: {issue_url}")
        
        print("🔗 Anexando Issue ao cartão do Trello...")
        attach_url_to_trello_card(card['id'], issue_url)
        print("✅ Anexo concluído!")

if __name__ == "__main__":
    main()
