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

def menu():
    while True:
        print("\n===== GESTOR DE PARTILHAS NFS =====")
        print("1️⃣  Listar partilhas")
        print("2️⃣  Criar partilha")
        print("3️⃣  Alterar partilha")
        print("4️⃣  Eliminar partilha")
        print("5️⃣  Desativar partilha")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            listar_partilhas()
        elif escolha == '2':
            criar_partilha()
        elif escolha == '3':
            alterar_partilha()
        elif escolha == '4':
            eliminar_partilha()
        elif escolha == '5':
            desativar_partilha()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()