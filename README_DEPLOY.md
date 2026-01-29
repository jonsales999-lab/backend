# Instruções para Deploy na Render

Este projeto foi reorganizado e corrigido para facilitar o deploy direto na Render.

## O que foi feito:
1. **Reorganização de Pastas**: Todos os arquivos da pasta `api/` foram movidos para a raiz. Isso evita erros de importação e simplifica o comando de inicialização.
2. **Correção de Importações**: Todos os arquivos `.py` foram atualizados para usar importações diretas (ex: `from models import ...` em vez de `from .models import ...`).
3. **Configuração de CORS**: O arquivo `main.py` foi atualizado para permitir conexões do seu domínio `https://ecoplaybrasil.com`.
4. **Conexão com Banco de Dados**: O arquivo `models.py` foi ajustado para suportar URLs do MySQL da Railway (adicionando automaticamente o driver `mysql+mysqlconnector://` se necessário).
5. **Arquivo render.yaml**: Atualizado para refletir a nova estrutura.

## Como fazer o Deploy:
1. Suba todo o conteúdo desta pasta para um novo repositório no seu **GitHub**.
2. Na **Render**, crie um novo "Web Service".
3. Conecte seu repositório do GitHub.
4. A Render detectará automaticamente o arquivo `render.yaml` e configurará o ambiente.
5. **IMPORTANTE**: Você deve configurar as seguintes Variáveis de Ambiente (Environment Variables) no painel da Render:
   - `DATABASE_URL`: A URL de conexão do seu banco na Railway (ex: `mysql://user:pass@host:port/db`).
   - `SECRET_KEY`: Uma chave aleatória para segurança dos tokens JWT.
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `60` (ou o tempo que desejar).

## Dependências:
As dependências foram corrigidas no arquivo `requirements.txt`. Certifique-se de que a Render use a versão do Python 3.9 ou superior.
