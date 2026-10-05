# Configuração do Quadro Trello: QA & Automation Portfolio

Este documento serve como guia para realizar o setup automático do seu quadro de QA no Trello usando Python e como realizar integrações manuais com o GitHub.

## 1. Obtendo suas Credenciais da API (API Key & Token)

Para que o script em Python funcione, você precisa gerar credenciais de acesso na plataforma para desenvolvedores do Trello:

1. Acesse o portal de Power-Ups de administração do Trello: [https://trello.com/power-ups/admin](https://trello.com/power-ups/admin).
2. Selecione seu workspace e crie um novo aplicativo (ou utilize um existente).
3. No menu lateral esquerdo, clique na aba **"API Key"** (Chave de API).
4. No topo dessa página, você verá sua **Chave de API** (uma string de 32 caracteres). Copie-a.
5. Logo abaixo da chave, procure o link com a palavra **"Token"** no texto que diz: *"Se você deseja criar um aplicativo para si mesmo... é possível gerar um token manualmente."*
6. Clique em "Token", clique em **Permitir** na aba que se abrir e copie a string longa fornecida (começa com "ATTA...").

Crie uma cópia do arquivo `.env.example` renomeando-o para `.env` no mesmo diretório do script, e preencha com as suas credenciais recém geradas:
```bash
TRELLO_API_KEY=sua_chave_copiada
TRELLO_TOKEN=seu_token_copiado
```

## 2. Executando o Script de Scaffold

Você precisará das bibliotecas `requests` e `python-dotenv` para rodar o script. 
No seu terminal, execute:

```bash
# Instale as dependências
pip install requests python-dotenv

# Execute a criação do quadro
python setup_trello_board.py
```

Isso fará o scaffold automático de todo o quadro, com as listas "Backlog" até "Bugs", as etiquetas padronizadas por cores e os cartões iniciais.

## 3. Configurando a Integração com GitHub (Manual)

### Habilitando o GitHub Power-Up
Para associar seus cartões a Commits, Pull Requests e Issues, ative o Power-Up do GitHub:

1. Abra o recém-criado quadro "QA & Automation Portfolio" no seu navegador.
2. No menu superior, clique em **Power-Ups** (ícone de um foguete ou em "Adicionar Power-Up").
3. Busque por **"GitHub"** e clique em **Adicionar**.
4. Autorize o Trello a acessar sua conta no GitHub (ele vai pedir o login e consentimento do OAuth do GitHub).
5. Vincule o(s) repositório(s) do seu portfólio de QA que você deseja gerenciar dentro deste quadro.

### Automatizando Criação de Issues (Regra do Butler)
Você pode usar a automação nativa do Trello (Butler) para criar uma Issue automaticamente no GitHub toda vez que você mover um cartão para a lista "Bugs":

1. No menu superior direito do quadro do Trello, clique em **Automação** (ícone do raio).
2. Vá em **Regras** (Rules) e clique em **Criar Regra**.
3. **Gatilho (Trigger):**
   - Selecione a categoria *Movimentação de Cartão*.
   - Configure: *"Quando um cartão for movido para a lista **Bugs** por qualquer pessoa..."* e clique no botão verde `(+)`.
4. **Ação (Action):**
   - Vá até as integrações ou clique em **GitHub** (caso ele esteja listado nas ações disponíveis após o Power-Up configurado).
   - *Nota: Na versão atual do Butler, pode ser necessário criar uma Issue via Trello diretamente pelos botões do Power-Up, pois as ações do GitHub no Butler podem exigir a conta Premium/Enterprise vinculada.*
   - Alternativa nativa usando comandos webhooks ou actions básicas: crie a ação *"Criar Issue no repositório vinculado com o título do cartão e com o link do cartão na descrição"*.
5. Salve a regra. A partir de agora, o workflow de QA enviará os registros diretamente para seu repositório quando um card cair na lista de Bugs!
