"""
Laboratório Educacional DIO - Código Vulnerável a SQL Injection
Arquivo: lab/app_vulneravel.py

ATENÇÃO: Este código foi desenvolvido exclusivamente para fins de estudo e teste de segurança.
Ele simula uma autenticação insegura vulnerável a CWE-89 (SQL Injection).
"""

import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT)")
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', 'SenhaForte123!')")
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES ('aluno', 'dio123')")
    conexao.commit()
    return conexao

def login_vulneravel(conexao, usuario_input, senha_input):
    cursor = conexao.cursor()
    
    # ❌ VULNERABILIDADE (CWE-89): Concatenação direta de strings na consulta SQL
    # Permite que um invasor altere a lógica da query (ex: usuario_input = "admin' --")
    query = f"SELECT * FROM usuarios WHERE usuario = '{usuario_input}' AND senha = '{senha_input}'"
    print(f"[DEBUG QUERY INSEGURA]: {query}")
    
    cursor.execute(query)
    resultado = cursor.fetchone()
    return resultado is not None

if __name__ == "__main__":
    db = inicializar_banco()
    print("=== Teste de Autenticação Insegura ===")
    
    # Tentativa de bypass usando payload clássico de SQL Injection
    payload_bypass = "admin' --"
    senha_qualquer = "qualquer_coisa"
    
    sucesso = login_vulneravel(db, payload_bypass, senha_qualquer)
    if sucesso:
        print("[ALERTA] Login autenticado com sucesso via SQL Injection Bypass!")
    else:
        print("[FALHA] Credenciais inválidas.")
