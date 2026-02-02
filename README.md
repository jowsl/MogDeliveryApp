# FFXIV Market Board Notifier

Monitor automático de preços do Market Board do Final Fantasy XIV usando a API do [Universalis](https://universalis.app/). Utilizo para automatizar as notificações caso o preço atinja um valor desejado

## Funcionalidades

- **Monitoramento Contínuo**: Verifica preços automaticamente a cada ~10 minutos
- **Alertas Discord**: Notificações instantâneas via Webhook quando o preço alvo é atingido
- **Persistência**: Lista de itens salva em `itens.txt` (formato JSON)
- **Adicionar Items em Tempo Real**: Janela interativa de 30 segundos entre ciclos

## Requisitos

- **Python**: 3.8 ou superior
- **Sistema Operacional**: Linux ou macOS
  - ⚠️ **Windows**: O script usa `signal.SIGALRM` que não é suportado nativamente. Use WSL (Windows Subsystem for Linux) ou adapte o código para usar `threading`
- **Dependências**: `requests`

## Configuração

### 1. Configure o Discord Webhook

Edite o arquivo `universalis.py` e substitua a URL do webhook:

```python
discord_url = "https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"
```

**Como criar um Webhook no Discord:**
1. Vá nas configurações do seu servidor Discord
2. Navegue até "Integrações" → "Webhooks"
3. Clique em "Novo Webhook"
4. Escolha o canal e copie a URL

### 2. (Opcional) Ajuste o Data Center

Por padrão, o script monitora o Data Center **Crystal**. Para mudar:

```python
# Na função priceVerifier, altere a linha para que SEU_DC seja o nome correto do datacenter:
response = requests.get(f"https://universalis.app/api/v2/SEU_DC/{item_id}")
```

**Data Centers disponíveis**: Aether, Crystal, Dynamis, Primal, Chaos, Light, Materia, Meteor, Elemental, Gaia, Mana

## Como Usar

1. **Inicie o script**:
```bash
python universalis.py
```

2. **Fluxo de operação**:
   - O script carrega itens salvos em `itens.txt`
   - Verifica os preços de todos os itens monitorados
   - Abre janela interativa de 30 segundos:
     - Pressione **Enter** para adicionar um novo item
     - Não faça nada para continuar o monitoramento
   - Aguarda ~10 minutos antes do próximo ciclo

3. **Adicionar um item**:
   - **ID do Item**: Encontre em [FFXIV Teamcraft](https://ffxivteamcraft.com/) ou [Garland Tools](https://www.garlandtools.org/)
   - **Preço Máximo**: Valor em gil que você quer pagar
   - **Nome**: Nome do item para referência

### Exemplo de Uso

```
Enter para adicionar outro item: [pressiona Enter]
Digite o ID do item: 36112
Digite o preco maximo que você quer pagar: 50000
Digite o nome do item: Windtea Leaves
```

**Formato do `itens.txt`**:
```json
[
  {
    "id": 36112,
    "max": 50000,
    "nome": "Windtea Leaves"
  }
]
```

##  Importante

### Limites da API
- Respeite os rate limits do Universalis
- Intervalo de 10 minutos entre verificações

## Features futuras
- Tratar o app epara que funcione como um chatbot que pode interagir por comandos via discord.
- Formular uma versão interativa com interface para rodar tanto no linux quando no windows.

## Licença

Este projeto é para fins educacionais e pessoais. Use por sua conta e risco.

## Créditos

- API: [Universalis](https://universalis.app/)
- Dados do jogo: Square Enix / Final Fantasy XIV
