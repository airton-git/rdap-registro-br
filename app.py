import requests
import time
from datetime import datetime
import sys
import os

last_time = datetime.now()

# ====== ARQUIVO TXT - domain.txt ======

# Obtém o diretório do script atual
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# Combina o diretório do script com o nome do arquivo.
# O arquivo domain.txt deve conter 1 dominio por linha.

file_path = os.path.join(diretorio_script, 'domain.txt')

# Caminho para salvar o arquivo de resultados
result_file_path = os.path.join(diretorio_script, 'resultados.txt')

# Lista de dominios
domain_lista = []

# Carrega a lista de domínios do arquivo domain.txt
with open(file_path, 'r') as file:
    for line in file:
        domain_lista.append(line.strip())

# ====== FINAL ARQUIVO TXT ======

# Função para fazer a consulta no servidor RDAP do registro.br


def query_rdap(domain):
    rdap_url = f"https://rdap.registro.br/domain/{domain}"
    response = requests.get(rdap_url)

    # Consulta bem-sucedida (código 200)
    if response.status_code == 200:
        print(f"Domínio: {domain} - Existe (200)")
        return domain, 200

    # Domínio não encontrado (código 404)
    elif response.status_code == 404:
        print(f"Domínio: {domain} - Não existe (404)")
        return domain, 404

    # Bloqueio pelo servidor RDAP (código 403)
    elif response.status_code == 403:
        print(f"\n==== Bloqueado - Código: {response.status_code} ====\n")
        print("Encerrando aplicação!")
        sys.exit()

    # Outros erros
    else:
        print(f"Erro ao consultar RDAP para o domínio {
              domain}. Código de status: {response.status_code}")
        return domain, response.status_code

# Função para salvar o resultado em um arquivo de texto


def salvar_resultado(domain, status):
    with open(result_file_path, 'a') as result_file:
        result_file.write(f"{domain};{status}\n")


# Verifica se há domínios a serem verificados
if not domain_lista:
    print("\nSem domínios para verificar! Aplicação encerrada.\n")
    sys.exit()

# Processa cada domínio da lista
for domain in domain_lista:
    domain_name, status = query_rdap(domain)

    # Salva o resultado da consulta no arquivo
    salvar_resultado(domain_name, status)

    # Aguarde 2 segundos antes da próxima consulta
    time.sleep(2)
