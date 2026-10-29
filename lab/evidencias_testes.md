# Evidências e Transcrições dos Testes do DIO Agent

Este documento registra os testes práticos de validação da nova skill `vulnerability-analysis` e da persona de mentor de segurança implementadas no **DIO Agent**.

---

## 🧪 Teste 1: Análise de Código com SQL Injection (`lab/app_vulneravel.py`)

### 1. Entrada do Estudante:
> *"Oi DIO Agent, sou iniciante em Python e montei essa função de login para um sisteminha interno. Dá uma olhada no código, está seguro?"*
> ```python
> def login(conexao, usuario_input, senha_input):
>     cursor = conexao.cursor()
>     query = f"SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND senha = '{senha_input}'"
>     cursor.execute(query)
>     return cursor.fetchone() is not None
> ```

### 2. Resposta do DIO Agent (com a skill `vulnerability-analysis` ativa):
> **DIO Agent:**  
> *"Olá! Muito bacana você estar implementando seu fluxo de autenticação em Python. Antes de analisarmos a sintaxe e sugerirmos qualquer código, como mentor de segurança eu preciso te fazer duas perguntinhas rápidas de contexto:*
> 1. *Esse sistema roda apenas localmente na sua máquina para estudos, ou você planeja disponibilizá-lo em uma rede interna/web?*
> 2. *Que tipo de dados esse banco armazena ou pretende armazenar futuramente?*
> 
> *Entender o contexto é o primeiro passo de qualquer análise de risco profissional!"*

### 3. Resposta do Estudante:
> *"É um projeto de estudos que pretendo colocar na nuvem em breve para testar com meus colegas de faculdade."*

### 4. Condução da Análise pelo Agente:
> **DIO Agent:**  
> *"Excelente contexto! Como você pretende expor a aplicação na nuvem, temos um ponto de atenção crítico aqui.*
> 
> #### 1. Identificação da Falha
> - **Vulnerabilidade:** SQL Injection (Injeção de SQL) - **CWE-89**.
> - **Mapeamento MITRE ATT&CK:** **T1190** (*Exploit Public-Facing Application*).
> - **Mapeamento OWASP:** **A03:2021 – Injection**.
> 
> #### 2. Mecânica do Problema
> *Você utilizou uma f-string (`f"SELECT ... '{usuario_input}'"`) para montar a query. Quando fazemos isso, o interpretador do banco de dados confunde os dados fornecidos pelo usuário com as instruções da linguagem SQL. Se alguém digitar `admin' --` no campo de usuário, a consulta final se tornará:*
> ```sql
> SELECT * FROM usuarios WHERE usuario = 'admin' --' AND senha = '...'
> ```
> *Os dois traços `--` comentam o resto da verificação de senha. Qualquer um entraria como administrador sem saber a senha!*
> 
> #### 3. Matriz de Avaliação de Risco
> | Critério | Classificação | Justificativa |
> | :--- | :--- | :--- |
> | **Impacto** | **Crítico** | Quebra total de Confidencialidade e Integridade (Tríade CID), permitindo bypass de autenticação e leitura de tabelas. |
> | **Probabilidade** | **Alta** | Falha trivial de detectar e explorar com ferramentas automáticas. |
> | **Severidade Geral** | **CRÍTICA** | Exposição pública sem autenticação confiável. |
> 
> #### 4. Como Corrigir (Parametrização)
> *A regra de ouro é: **nunca concatene strings em comandos SQL**. Utilize **Prepared Statements** (consultas parametrizadas). O driver do banco enviará a estrutura da query e os dados em canais separados:*
> 
> ```python
> # ✅ Forma Segura:
> query = "SELECT id, usuario FROM usuarios WHERE usuario = ? AND hash_senha = ?"
> cursor.execute(query, (usuario_input, hash_senha))
> ```
> 
> *Além disso, observe que armazenar senhas em texto puro também é inseguro. Recomendamos aplicar hash criptográfico (como SHA-256 ou bcrypt). Veja a implementação completa corrigida no arquivo [`lab/app_seguro.py`](./app_seguro.py).*

---

## 🧪 Teste 2: Cenário de Infraestrutura (Servidor Ubuntu Exposto)

### 1. Entrada do Estudante:
> *"DIO Agent, subi um servidor Ubuntu de laboratório na AWS e ele já está exposto na internet. Quais comandos você me passa para eu proteger a máquina agora?"*

### 2. Resposta do DIO Agent (Recusando prescrições cegas):
> **DIO Agent:**  
> *"Calma aí! Um bom profissional de segurança nunca começa executando comandos de firewall ou desativando serviços sem mapear o terreno primeiro. Se você bloquear portas sem saber o que precisa rodar, pode perder o acesso remoto (SSH) à sua máquina.*
> 
> *Antes de rodarmos qualquer comando, me responda:*
> 1. *Como você está acessando esse servidor: por chave SSH (.pem/.pub) ou por usuário e senha convencional?*
> 2. *Quais serviços essa máquina vai hospedar (um servidor web na porta 80/443, banco de dados, API)?*
> 3. *Essa máquina de laboratório tem acesso à sua rede doméstica/corporativa via VPN ou está isolada?*
> 
> *Com essas respostas, montamos um plano de hardening seguro e cirúrgico, sem risco de você se trancar para fora!"*

---

## 📊 Comparativo: DIO Agent com Skill vs. Chat Genérico

| Critério | Chat Genérico (Sem Skill) | DIO Agent (Com `vulnerability-analysis`) |
| :--- | :--- | :--- |
| **Primeira Reação** | Cospe blocos gigantescos de código ou listas de comandos de terminal imediatamente. | Faz perguntas de contexto e avalia o ambiente antes de prescrever qualquer solução. |
| **Modelagem de Risco** | Apenas diz "isso é vulnerável". | Classifica formalmente Impacto, Probabilidade e Severidade (Tríade CID). |
| **Padrões da Indústria** | Raramente cita referências formais. | Mapeia formalmente para **CWE**, **OWASP Top 10** e **MITRE ATT&CK**. |
| **Didática** | Entrega o código pronto para copiar e colar. | Explica a causa-raiz, guia o raciocínio e propõe controles em camadas (*Defense in Depth*). |
