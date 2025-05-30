#!/usr/bin/env python3
import os
import subprocess
import datetime
import sys

BIND_DIR = "/var/named"
NAMED_CONF_PATH = "/etc/named.conf"

def listar_zonas_master():
    zonas = []
    with open(NAMED_CONF_PATH, "r") as f:
        for line in f:
            if line.strip().startswith('zone "') and 'type master;' in line:
                nome = line.split('"')[1]
                zonas.append(nome)
    print("\n🌐 Zonas master existentes:")
    if zonas:
        for z in zonas:
            print(f" - {z}")
    else:
        print(" (nenhuma zona master configurada)")
    return zonas

def criar_zona_master(dominio=None, ip=None):
    if dominio is None:
        dominio = input("Domínio: ").strip()
    if ip is None:
        ip = input("IP: ").strip()
        
    zona_filename = f"{dominio}.zone"
    zona_path = os.path.join(BIND_DIR, zona_filename)

    # 1. Criar ficheiro de zona
    zona_conteudo = f"""
$TTL 86400
@   IN  SOA ns1.{dominio}. admin.{dominio}. (
        {datetime.datetime.now().strftime("%Y%m%d")}01 ; Serial
        3600        ; Refresh
        1800        ; Retry
        604800      ; Expire
        86400       ; Minimum TTL
)
@       IN  NS      ns1.{dominio}.
@       IN  A       {ip}
ns1     IN  A       {ip}
www     IN  A       {ip}
"""

    with open(zona_path, "w") as f:
        f.write(zona_conteudo.strip() + "\n")

    os.chmod(zona_path, 0o644)
    print(f"✅ Ficheiro de zona criado: {zona_path}")

    # 2. Adicionar entrada em /etc/named.conf se não existir
    zona_conf = f"""
zone "{dominio}" IN {{
    type master;
    file "{zona_filename}";
}};
"""

    with open(NAMED_CONF_PATH, "r") as f:
        named_conf = f.read()

    if dominio not in named_conf:
        with open(NAMED_CONF_PATH, "a") as f:
            f.write("\n" + zona_conf.strip() + "\n")
        print(f"✅ Zona adicionada ao named.conf")
    else:
        print(f"ℹ️ Zona já existe no named.conf")

    # 3. Reiniciar serviço
    try:
        subprocess.run(["systemctl", "restart", "named"], check=True)
        print("🔁 Serviço 'named' reiniciado com sucesso.")
    except subprocess.CalledProcessError:
        print("❌ Erro ao reiniciar o serviço 'named'.")

def eliminar_zona_master():
    zonas = listar_zonas_master()
    if not zonas:
        print("⚠️ Não existem zonas master para eliminar.")
        return
    dominio = input("\n🗑️ Indique o domínio da zona a eliminar: ").strip()
    if dominio not in zonas:
        print(f"❌ A zona '{dominio}' não existe!")
        return

    # Remover bloco da zona do named.conf
    with open(NAMED_CONF_PATH, "r") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.strip().startswith(f'zone "{dominio}"'):
            skip = True
        if not skip:
            new_lines.append(line)
        if skip and line.strip().endswith("};"):
            skip = False
    with open(NAMED_CONF_PATH, "w") as f:
        f.writelines(new_lines)
    print(f"🗑️ Zona removida do {NAMED_CONF_PATH}")

    # Remover ficheiro de zona
    zona_filename = f"{dominio}.zone"
    zona_path = os.path.join(BIND_DIR, zona_filename)
    if os.path.exists(zona_path):
        os.remove(zona_path)
        print(f"🗑️ Ficheiro de zona removido: {zona_path}")

    # Reiniciar serviço
    try:
        subprocess.run(["systemctl", "restart", "named"], check=True)
        print("🔁 Serviço 'named' reiniciado com sucesso.")
    except subprocess.CalledProcessError:
        print("❌ Erro ao reiniciar o serviço 'named'.")

def menu():
    while True:
        print("\n===== GESTOR DE ZONAS MASTER DNS =====")
        print("1️⃣  Criar zona master")
        print("2️⃣  Eliminar zona master")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            criar_zona_master(dominio, ip)
        elif escolha == '2':
            eliminar_zona_master()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--auto":
        criar_zona_master(sys.argv[2], sys.argv[3])
    else:
        # menu normal
        menu()