#!/usr/bin/env python3
import os
import subprocess

EXPORTS_FILE = "/etc/exports"

def listar_partilhas(mostrar_todas=False):
    print("\n📂 Partilhas NFS existentes:")
    with open(EXPORTS_FILE, "r") as f:
        linhas = [l.rstrip('\n') for l in f if l.strip() and (mostrar_todas or not l.strip().startswith("#"))]
    if linhas:
        for idx, l in enumerate(linhas, 1):
            print(f"{idx} - {l}")
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
    partilhas = listar_partilhas(mostrar_todas=True)
    if not partilhas:
        return
    idx = int(input("Índice da partilha a eliminar: ").strip()) - 1
    if idx < 0 or idx >= len(partilhas):
        print("❌ Índice inválido.")
        return
    linha_remover = partilhas[idx]
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = [l for l in linhas if l.rstrip('\n') != linha_remover]
    with open(EXPORTS_FILE, "w") as f:
        f.writelines(novas)
    print(f"🗑️ Partilha eliminada: {linha_remover}")
    subprocess.run(["exportfs", "-ra"])
    print("🔄 NFS recarregado.")

def alterar_partilha():
    partilhas = listar_partilhas(mostrar_todas=True)
    if not partilhas:
        return
    idx = int(input("Índice da partilha a alterar: ").strip()) - 1
    if idx < 0 or idx >= len(partilhas):
        print("❌ Índice inválido.")
        return
    linha_antiga = partilhas[idx]
    print(f"Configuração atual: {linha_antiga}")
    caminho = linha_antiga.lstrip("#").strip().split()[0]
    clientes = input("Nova configuração de clientes (ex: 192.168.1.0/24(rw,sync,no_root_squash)): ").strip()
    linha_nova = f"{caminho} {clientes}"
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = []
    for l in linhas:
        if l.rstrip('\n') == linha_antiga:
            novas.append(linha_nova + "\n")
        else:
            novas.append(l)
    with open(EXPORTS_FILE, "w") as f:
        f.writelines(novas)
    print(f"✏️ Partilha alterada: {linha_nova}")
    subprocess.run(["exportfs", "-ra"])
    print("🔄 NFS recarregado.")

def desativar_partilha():
    partilhas = listar_partilhas()
    if not partilhas:
        return
    idx = int(input("Índice da partilha a desativar: ").strip()) - 1
    if idx < 0 or idx >= len(partilhas):
        print("❌ Índice inválido.")
        return
    linha_desativar = partilhas[idx]
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = []
    desativada = False
    for l in linhas:
        if l.rstrip('\n') == linha_desativar and not l.strip().startswith("#"):
            novas.append(f"# {l}")
            desativada = True
        else:
            novas.append(l)
    if desativada:
        with open(EXPORTS_FILE, "w") as f:
            f.writelines(novas)
        print(f"🚫 Partilha desativada: {linha_desativar}")
        subprocess.run(["exportfs", "-ra"])
        print("🔄 NFS recarregado.")
    else:
        print("❌ Partilha não encontrada ou já desativada.")

def ativar_partilha():
    partilhas = listar_partilhas(mostrar_todas=True)
    # Só mostrar as desativadas (comentadas)
    desativadas = [(i, l) for i, l in enumerate(partilhas) if l.strip().startswith("#")]
    if not desativadas:
        print("Não há partilhas desativadas.")
        return
    print("\nPartilhas desativadas:")
    for idx, (i, l) in enumerate(desativadas, 1):
        print(f"{idx} - {l}")
    escolha = int(input("Índice da partilha a ativar: ").strip()) - 1
    if escolha < 0 or escolha >= len(desativadas):
        print("❌ Índice inválido.")
        return
    linha_desativada = desativadas[escolha][1]
    with open(EXPORTS_FILE, "r") as f:
        linhas = f.readlines()
    novas = []
    ativada = False
    for l in linhas:
        if l.rstrip('\n') == linha_desativada:
            novas.append(l.lstrip("# ").rstrip() + "\n")
            ativada = True
        else:
            novas.append(l)
    if ativada:
        with open(EXPORTS_FILE, "w") as f:
            f.writelines(novas)
        print(f"✅ Partilha ativada: {linha_desativada.lstrip('# ').rstrip()}")
        subprocess.run(["exportfs", "-ra"])
        print("🔄 NFS recarregado.")
    else:
        print("❌ Partilha não encontrada ou já ativa.")

def menu():
    while True:
        print("\n===== GESTOR DE PARTILHAS NFS =====")
        print("1️⃣  Listar partilhas ativas")
        print("2️⃣  Criar partilha")
        print("3️⃣  Alterar partilha")
        print("4️⃣  Eliminar partilha")
        print("5️⃣  Desativar partilha")
        print("6️⃣  Ativar partilha")
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
        elif escolha == '6':
            ativar_partilha()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()