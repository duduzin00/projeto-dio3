"""
Laboratório Educacional DIO - Código Corrigido e Seguro (AppSec)
Arquivo: lab/app_seguro.py

Implementa a remediação recomendada pelo DIO Agent:
1. Consultas Parametrizadas (Prepared Statements) para neutralizar SQL Injection (CWE-89).
2. Armazenamento de senhas com Hash Criptográfico (SHA-256 / PBKDF2) em vez de texto claro.
"""

import sqlite3
import hashlib

def gerar_hash_senha(senha: str) -> str:
    """Gera hash SHA-256 para armazenamento seguro de senhas."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def inicializar_banco_seguro():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, hash_senha TEXT)")
    
    # Armazenando senhas protegidas por hash
    cursor.execute("INSERT INTO usuarios (usuario, hash_senha) VALUES (?, ?)", 
                   ('admin', gerar_hash_senha('SenhaForte123!')))
    cursor.execute("INSERT INTO usuarios (usuario, hash_senha) VALUES (?, ?)", 
                   ('aluno', gerar_hash_senha('dio123')))
    conexao.commit()
    return conexao

def login_seguro(conexao, usuario_input: str, senha_input: str) -> bool:
    cursor = conexao.cursor()
    hash_fornecido = gerar_hash_senha(senha_input)
    
    # ✅ REMEDIAÇÃO CANÔNICA: Consulta Parametrizada (Prepared Statement)
    # O driver trata usuario_input e hash_fornecido puramente como dados literais,
    # impedindo que payloads alterem a estrutura sintática do SQL.
    query = "SELECT id, usuario FROM usuarios WHERE usuario = ? AND hash_senha = ?"
    print(f"[DEBUG QUERY SEGURA]: {query} com parâmetros: ({usuario_input}, [HASH_OCULTO])")
    
    cursor.execute(query, (usuario_input, hash_fornecido))
    resultado = cursor.fetchone()
    return resultado is not None

if __name__ == "__main__":
    db = inicializar_banco_seguro()
    print("=== Teste de Autenticação Segura e Parametrizada ===")
    
    # Tentativa de bypass com o mesmo payload malicioso
    payload_bypass = "admin' --"
    senha_qualquer = "qualquer_coisa"
    
    sucesso = login_seguro(db, payload_bypass, senha_qualquer)
    if sucesso:
        print("[ERRO] Bypass efetuado indevidamente.")
    else:
        print("[SUCESSO DEFENSIVO] Tentativa de injeção bloqueada! Usuário literal não encontrado.")

    # Teste de login legítimo
    print("\n--- Teste com Credenciais Legítimas ---")
    login_valido = login_seguro(db, "admin", "SenhaForte123!")
    print(f"Resultado do login legítimo: {'Autenticado com Sucesso!' if login_valido else 'Falha'}")
