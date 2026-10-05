# Setup: Automação Trello 🔄 GitHub Actions

Acabei de criar a infraestrutura necessária para que o GitHub aja como um robô que fiscaliza seu Trello de graça.

## Arquivos Criados
1. **`scripts/sync_trello_github.py`**: A inteligência da integração. Um script Python enxuto usando a API nativa.
2. **`.github/workflows/trello_sync.yml`**: A esteira de automação (CI/CD) que manda o GitHub rodar esse script a cada 10 minutos automaticamente.

## Como Colocar Para Rodar

### Passo 1: Fazer o Push para o GitHub
Para que o GitHub Actions identifique o fluxo, você precisa comitar e dar push dessas pastas `scripts/` e `.github/` para o seu repositório remoto.

### Passo 2: Configurar as Variáveis (Secrets) no GitHub
Como nosso código está em um repositório, não subimos o arquivo `.env` para a nuvem por segurança. Você precisa colocar as chaves direto nas configurações secretas do repositório:

1. Vá até a página do seu repositório no **GitHub**.
2. Clique em **Settings** (Configurações) no menu superior.
3. No menu lateral esquerdo, vá em **Secrets and variables** > **Actions**.
4. Clique no botão verde **New repository secret** e crie os três secrets abaixo:
   - Nome: `TRELLO_API_KEY` | Valor: *(cole a mesma chave usada antes, que começa com 30516...)*
   - Nome: `TRELLO_TOKEN` | Valor: *(cole o token longo, que começa com ATTA...)*
   - Nome: `TRELLO_BOARD_ID` | Valor: `O2CfizDA` *(este é o ID curto do quadro que criamos)*
   
*(Nota: O `GITHUB_TOKEN` não precisa ser criado por você, o próprio GitHub injeta ele de forma segura nas rodadas).*

### Passo 3: Testar a Integração
1. Vá no seu **Trello**.
2. Crie um cartão qualquer na lista "Bugs" (Ex: *"Erro no login com usuário bloqueado"*).
3. Vá no **GitHub** > Aba **Actions**.
4. Clique no fluxo **"Trello Bugs to GitHub Issues Sync"**.
5. Você pode esperar ele rodar sozinho (demora até 10 minutos) ou clicar em **Run workflow** para forçar ele a rodar agora mesmo.

Assim que a "bolinha verde" brilhar na Action, olhe na aba **Issues** do seu repositório: O Bug vai estar lá, e se você olhar no Trello, o script vai ter colado o link da Issue no seu cartão!
