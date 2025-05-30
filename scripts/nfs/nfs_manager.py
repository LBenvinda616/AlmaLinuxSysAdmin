#!/usr/bin/env python3
import os
import subprocess

EXPORTS_FILE = "/etc/exports"

def listar_partilhas():
    print("\n📂 Partilhas NFS existentes:")
    with open(EXPORTS_FILE, "r") as f:
        linhas = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    if linhas:
        for l in linhas:
            print(f" - {l}")
    else:
        print(" (nenhuma partilha configurada)")
    return linhas

def criar_partilha():
    caminho = input("Diretório a partilhar (ex: /srv/nfs/dados): ").strip()
    clientes = input("Clientes autorizados (ex: 192.168.1.0/24(rw,sync,no_root_squash)): ").strip()
    linha = f"{caminho} {clientes}"
    with open(EXPORTS_FILE, "a") as f:
        f.write(linha + "\n")
    print(f"✅ Partilha criada: {linha}")
    subprocess.run(["exportfs", "-ra"])
    print("🔄 NFS recarregado.")

def eliminar_partilha():
    partilhas = listar_partilhas()
    if not partilhas:
        return
    caminho = input("Diretório da partilha a eliminar: ").strip()
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = [l for l in linhas if not l.strip().startswith(caminho)]
    with open(EXPORTS_FILE, "w") as f:
        f.writelines(novas)
    print(f"🗑️ Partilha eliminada: {caminho}")
    subprocess.run(["exportfs", "-ra"])
    print("🔄 NFS recarregado.")

def alterar_partilha():
    partilhas = listar_partilhas()
    if not partilhas:
        return
    caminho = input("Diretório da partilha a alterar: ").strip()
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = []
    alterada = False
    for l in linhas:
        if l.strip().startswith(caminho):
            print(f"Configuração atual: {l.strip()}")
            clientes = input("Nova configuração de clientes (ex: 192.168.1.0/24(rw,sync,no_root_squash)): ").strip()
            novas.append(f"{caminho} {clientes}\n")
            alterada = True
        else:
            novas.append(l)
    if alterada:
        with open(EXPORTS_FILE, "w") as f:
            f.writelines(novas)
        print(f"✏️ Partilha alterada: {caminho}")
        subprocess.run(["exportfs", "-ra"])
        print("🔄 NFS recarregado.")
    else:
        print("❌ Partilha não encontrada.")

def desativar_partilha():
    partilhas = listar_partilhas()
    if not partilhas:
        return
    caminho = input("Diretório da partilha a desativar: ").strip()
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = []
    desativada = False
    for l in linhas:
        if l.strip().startswith(caminho):
            novas.append(f"# {l}")
            desativada = True
        else:
            novas.append(l)
    if desativada:
        with open(EXPORTS_FILE, "w") as f:
            f.writelines(novas)
        print(f"🚫 Partilha desativada: {caminho}")
        subprocess.run(["exportfs", "-ra"])
        print("🔄 NFS recarregado.")
    else:
        print("❌ Partilha não encontrada.")

def reativar_zona_master():
    # Listar ficheiros de zona disponíveis
    zonas_ficheiro = [f for f in os.listdir(BIND_DIR) if f.endswith(".zone")]
    print("\n📂 Ficheiros de zona disponíveis em disco:")
    for z in zonas_ficheiro:
        print(f" - {z}")
    dominio = input("Introduz o nome do domínio a reativar (ex: exemplo.com): ").strip()
    zona_filename = f"{dominio}.zone"
    zona_path = os.path.join(BIND_DIR, zona_filename)
    if not os.path.exists(zona_path):
        print("❌ Ficheiro de zona não existe em disco.")
        return

    # Verificar se já existe no named.conf
    with open(NAMED_CONF_PATH, "r") as f:
        named_conf = f.read()
    if dominio in named_conf:
        print("ℹ️ Zona já está ativa no named.conf.")
        return

    zona_conf = f"""
zone "{dominio}" IN {{
    type master;
    file "{zona_filename}";
}};
"""
    with open(NAMED_CONF_PATH, "a") as f:
        f.write("\n" + zona_conf.strip() + "\n")
    print(f"✅ Zona reativada no named.conf")

    # Reiniciar serviço
    try:
        subprocess.run(["systemctl", "restart", "named"], check=True)
        print("🔁 Serviço 'named' reiniciado com sucesso.")
    except subprocess.CalledProcessError:
        print("❌ Erro ao reiniciar o serviço 'named'.")

# Atualiza o menu:
def menu():
    while True:
        print("\n===== GESTOR DE ZONAS MASTER DNS =====")
        print("1️⃣  Criar zona master")
        print("2️⃣  Eliminar zona master")
        print("3️⃣  Reativar zona master")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            dominio = input("Introduz o nome do domínio (ex: exemplo.com): ").strip()
            ip = input("Introduz o IP para o registo A (ex: 192.168.1.10): ").strip()
            criar_zona_master(dominio, ip)
        elif escolha == '2':
            eliminar_zona_master()
        elif escolha == '3':
            reativar_zona_master()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()