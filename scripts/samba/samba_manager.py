#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

SAMBA_CONFIG = "/etc/samba/smb.conf"

def reiniciar_samba():
    print("\n🔄 A reiniciar o serviço smb...")
    subprocess.run(["systemctl", "restart", "smb"], check=True)

def criar_partilha():
    nome = input("🔹 Nome da partilha: ").strip()
    caminho = input("📁 Caminho da pasta (ex: /srv/samba/partilha): ").strip()
    read_only = input("🔒 Só leitura? (s/n): ").lower().startswith('s')

    if not os.path.exists(caminho):
        os.makedirs(caminho)

    with open(SAMBA_CONFIG, "a") as f:
        f.write(f"""

[{nome}]
   path = {caminho}
   browseable = yes
   writable = {"no" if read_only else "yes"}
   guest ok = yes
   read only = {"yes" if read_only else "no"}
""")
    reiniciar_samba()
    print(f"✅ Partilha '{nome}' criada com sucesso.")

def eliminar_partilha():
    nome = input("🗑️ Nome da partilha a eliminar: ").strip()

    with open(SAMBA_CONFIG, "r") as f:
        linhas = f.readlines()

    inicio = None
    fim = None
    for i, linha in enumerate(linhas):
        if linha.strip() == f"[{nome}]":
            inicio = i
            for j in range(i+1, len(linhas)):
                if linhas[j].strip().startswith("[") or linhas[j].strip() == "":
                    fim = j
                    break
            break

    if inicio is not None:
        if fim is None:
            fim = len(linhas)
        del linhas[inicio:fim]
        with open(SAMBA_CONFIG, "w") as f:
            f.writelines(linhas)
        reiniciar_samba()
        print(f"❌ Partilha '{nome}' eliminada.")
    else:
        print(f"⚠️ Partilha '{nome}' não encontrada.")

def alterar_partilha():
    nome = input("✏️ Nome da partilha a alterar: ").strip()
    novo_caminho = input("📁 Novo caminho (enter para manter): ").strip()
    ro_input = input("🔒 Alterar para só leitura? (s/n ou enter para manter): ").lower().strip()

    with open(SAMBA_CONFIG, "r") as f:
        linhas = f.readlines()

    nova_config = []
    dentro_secao = False
    for linha in linhas:
        if linha.strip() == f"[{nome}]":
            dentro_secao = True
            nova_config.append(linha)
            continue
        if dentro_secao:
            if linha.strip().startswith("[") and not linha.strip().startswith(f"[{nome}]"):
                dentro_secao = False
                nova_config.append(linha)
                continue
            # Só altera as opções relevantes, mantendo as outras
            if linha.strip().startswith("path =") and novo_caminho:
                nova_config.append(f"   path = {novo_caminho}\n")
            elif linha.strip().startswith("writable =") and ro_input in ['s', 'n']:
                nova_config.append(f"   writable = {'no' if ro_input == 's' else 'yes'}\n")
            elif linha.strip().startswith("read only =") and ro_input in ['s', 'n']:
                nova_config.append(f"   read only = {'yes' if ro_input == 's' else 'no'}\n")
            else:
                nova_config.append(linha)
        else:
            nova_config.append(linha)

    with open(SAMBA_CONFIG, "w") as f:
        f.writelines(nova_config)

    reiniciar_samba()
    print(f"✏️ Partilha '{nome}' alterada com sucesso.")

def eliminar_partilha_por_codigo(nome):
    with open(SAMBA_CONFIG, "r") as f:
        linhas = f.readlines()

    inicio = None
    fim = None
    for i, linha in enumerate(linhas):
        if linha.strip() == f"[{nome}]":
            inicio = i
            for j in range(i+1, len(linhas)):
                if linhas[j].strip().startswith("[") or linhas[j].strip() == "":
                    fim = j
                    break
            break

    if inicio is not None:
        if fim is None:
            fim = len(linhas)
        del linhas[inicio:fim]
        with open(SAMBA_CONFIG, "w") as f:
            f.writelines(linhas)

def criar_partilha_personalizada(nome, caminho, read_only):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    with open(SAMBA_CONFIG, "a") as f:
        f.write(f"""

[{nome}]
   path = {caminho}
   browseable = yes
   writable = {"no" if read_only else "yes"}
   guest ok = yes
   read only = {"yes" if read_only else "no"}
""")
    reiniciar_samba()
    print(f"✅ Partilha '{nome}' alterada com sucesso.")

def desativar_partilha():
    nome = input("🚫 Nome da partilha a desativar: ").strip()
    with open(SAMBA_CONFIG, "r") as f:
        linhas = f.readlines()

    nova_config = []
    dentro_secao = False
    for linha in linhas:
        if linha.strip() == f"[{nome}]":
            dentro_secao = True
            nova_config.append(linha)
            continue
        if dentro_secao:
            if linha.strip().startswith("[") and not linha.strip().startswith(f"[{nome}]"):
                dentro_secao = False
                nova_config.append(linha)
                continue
            # Altera apenas as opções de ativação
            if linha.strip().startswith("browseable ="):
                nova_config.append("   browseable = no\n")
            elif linha.strip().startswith("writable ="):
                nova_config.append("   writable = no\n")
            elif linha.strip().startswith("available ="):
                nova_config.append("   available = no\n")
            else:
                nova_config.append(linha)
        else:
            nova_config.append(linha)

    # Se não existir a linha "available =", adiciona ao fim da secção
    if dentro_secao:
        nova_config.append("   available = no\n")

    with open(SAMBA_CONFIG, "w") as f:
        f.writelines(nova_config)

    reiniciar_samba()
    print(f"🚫 Partilha '{nome}' desativada.")

def montar_partilha_remota():
    remote_path = input("🌐 Caminho remoto (ex: //192.168.1.100/partilha): ").strip()
    local_path = input("📁 Caminho local para montagem (ex: /mnt/remota): ").strip()
    username = input("👤 Nome de utilizador: ").strip()
    password = input("🔑 Password: ").strip()

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    comando = [
        "mount.cifs",
        remote_path,
        local_path,
        "-o", f"username={username},password={password}"
    ]
    subprocess.run(comando, check=True)
    print(f"🔗 Partilha remota montada com sucesso em {local_path}.")

def ativar_partilha():
    nome = input("✅ Nome da partilha a ativar: ").strip()
    with open(SAMBA_CONFIG, "r") as f:
        linhas = f.readlines()

    nova_config = []
    dentro_secao = False
    for linha in linhas:
        if linha.strip() == f"[{nome}]":
            dentro_secao = True
            nova_config.append(linha)
            continue
        if dentro_secao:
            if linha.strip().startswith("[") and not linha.strip().startswith(f"[{nome}]"):
                dentro_secao = False
                nova_config.append(linha)
                continue
            # Só altera as opções de ativação, mantendo as outras
            if linha.strip().startswith("browseable ="):
                nova_config.append("   browseable = yes\n")
            elif linha.strip().startswith("writable ="):
                nova_config.append("   writable = yes\n")
            elif linha.strip().startswith("available ="):
                # Remove a linha "available = no" (opcional, pois default é yes)
                continue
            else:
                nova_config.append(linha)
        else:
            nova_config.append(linha)


    with open(SAMBA_CONFIG, "w") as f:
        f.writelines(nova_config)

    reiniciar_samba()
    print(f"✅ Partilha '{nome}' ativada com sucesso.")

# Adicione ao menu:
def menu():
    while True:
        print("\n===== GESTOR DE PARTILHAS SAMBA =====")
        print("1️⃣  Criar partilha")
        print("2️⃣  Eliminar partilha")
        print("3️⃣  Alterar partilha")
        print("4️⃣  Desativar partilha")
        print("5️⃣  Montar partilha remota")
        print("6️⃣  Ativar partilha")
        print("0️⃣  Sair")

        escolha = input("Selecione uma opção: ").strip()

        if escolha == '1':
            criar_partilha()
        elif escolha == '2':
            eliminar_partilha()
        elif escolha == '3':
            alterar_partilha()
        elif escolha == '4':
            desativar_partilha()
        elif escolha == '5':
            montar_partilha_remota()
        elif escolha == '6':
            ativar_partilha()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
