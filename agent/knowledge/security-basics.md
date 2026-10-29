# Fundamentos de Segurança da Informação e AppSec

Este documento serve como base de conhecimento conceitual para o **DIO Agent** ao apoiar estudantes em dúvidas de segurança cibernética e desenvolvimento seguro.

---

## 1. Tríade Fundamental: Vulnerabilidade, Ameaça e Risco

Para orientar estudantes corretamente, mantenha sempre clara a distinção entre esses três conceitos:

- **Vulnerabilidade**: É uma fraqueza, falha de projeto, brecha de implementação ou lacuna de configuração existente em um sistema, processo ou código-fonte.
  - *Exemplo*: Um código que concatena parâmetros diretamente em uma query SQL (CWE-89).
- **Ameaça (*Threat*)**: É qualquer evento, agente externo (hacker, malware, falha física) ou circunstância com potencial para causar danos ao explorar uma vulnerabilidade.
  - *Exemplo*: Um ator malicioso enviando payloads de SQL Injection (`' OR 1=1 --`).
- **Risco (*Risk*)**: É a probabilidade de uma ameaça explorar uma vulnerabilidade, multiplicada pela magnitude do impacto causado ao negócio ou aos dados:
  $$\text{Risco} = \text{Ameaça} \times \text{Vulnerabilidade} \times \text{Impacto}$$
  - *Exemplo*: Se o banco de dados contém dados pessoais de clientes e está exposto na internet, o risco é **Crítico**. Se está em uma VM isolada sem dados reais, o risco é **Baixo**.

---

## 2. A Tríade da Informação (CID / CIA Triad)

Toda análise de impacto em cibersegurança deve mensurar quais pilares da tríade foram comprometidos:

1. **Confidencialidade (*Confidentiality*)**:
   - Garantir que a informação seja acessível somente por indivíduos ou processos autorizados.
   - *Ameaças*: Vazamento de credenciais, espionagem, SQL Injection com extração de tabelas.
2. **Integridade (*Integrity*)**:
   - Garantir a exatidão, completude e proteção contra modificação não autorizada dos dados.
   - *Ameaças*: Adulteração de saldos em bancos de dados, desfiguração de sites (*defacement*), Man-in-the-Middle (MitM).
3. **Disponibilidade (*Availability*)**:
   - Garantir que os sistemas e dados estejam acessíveis aos usuários autorizados quando necessário.
   - *Ameaças*: Ataques de negação de serviço (DoS/DDoS), travamento de serviços, ransomware.

---

## 3. Princípios Fundamentais de Segurança Defensiva

Ao orientar estudantes, estimule a adoção dos seguintes princípios:

- **Defesa em Profundidade (*Defense in Depth*)**: Nunca confiar em uma única barreira. Combine validação no front-end, consultas parametrizadas no back-end, WAF no proxy e permissões restritas no banco de dados.
- **Menor Privilégio (*Principle of Least Privilege - PoLP*)**: Cada usuário, processo e aplicação deve possuir apenas os privilégios estritamente necessários para desempenhar sua função.
- **Não Confiança e Validação Rígida (*Zero Trust & Input Validation*)**: Nunca confiar nos dados recebidos do cliente (formulários, headers, cookies). Sempre validar tipo, tamanho e formato através de listas permitidas (*allowlists*).
- **Falha Segura (*Fail Secure*)**: Em caso de erro inesperado ou exceção no código, o sistema deve entrar em um estado seguro (ex: negar acesso por padrão), em vez de liberar privilégios ou exibir *stack traces* sensíveis ao usuário.
- **Parametrização de Consultas (*Prepared Statements*)**: A defesa canônica contra SQL Injection. Separa completamente a lógica do comando SQL dos dados enviados pelo usuário.

---

## 4. Frameworks e Padrões de Referência

- **OWASP Top 10**: Os dez riscos de segurança mais críticos em aplicações web (Injeção, Quebra de Controle de Acesso, Falhas Criptográficas, etc.).
- **MITRE ATT&CK**: Base de conhecimento global sobre táticas, técnicas e procedimentos (TTPs) reais utilizados por invasores.
- **CWE (Common Weakness Enumeration)**: Dicionário formal de tipos de fraquezas em software e hardware.
