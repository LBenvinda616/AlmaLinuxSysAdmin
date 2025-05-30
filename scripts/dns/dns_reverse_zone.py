#!/usr/bin/env python3
import os
import subprocess
import re
import sys
from shutil import copy2

ZONEDIR = "/var/named"
NAMED_CONF = "/etc/named.conf"

def ip_to_reverse_zone(ip):
    octetos = ip.split('.')
    if len(octetos) != 4:
        return None
    return f"{octetos[2]}.{octetos[1]}.{octetos[0]}.in-addr.arpa"

def listar_reverse_zones():
    zonas = []
    with open(NAMED_CONF, "r") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('zone "') and '.in-addr.arpa' in line:
            nome = line.split('"')[1]
            bloco = []
            i += 1
            while i < len(lines) and "};" not in lines[i]:
                bloco.append(lines[i])
                i += 1
            if any("type master;" in l for l in bloco):
                zonas.append(nome)
        i += 1
    print("\n🔄 Zonas reverse existentes:")
    if zonas:
        for z in zonas:
            print(f" - {z}")
    else:
        print(" (nenhuma zona reverse configurada)")
    return zonas

def criar_reverse_zone(ip=None):
    if ip is None:
        ip = input("Endereço IPv4 (ex: 192.168.1.10): ").strip()
        
    fqdn = input("FQDN (ex: host.exemplo.com.): ").strip()
    
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("❌ IP inválido.")
        return
    if not fqdn.endswith('.'):
        print("❌ O FQDN deve terminar com ponto.")
        return

    reverse_zone = ip_to_reverse_zone(ip)
    if not reverse_zone:
        print("❌ IP inválido para zona reverse.")
        return

    zone_file = os.path.join(ZONEDIR, f"{reverse_zone}.zone")

    # 1. Verifica se a zona já existe no named.conf
    with open(NAMED_CONF, "r") as f:
        named_conf = f.read()
    if reverse_zone in named_conf:
        print(f"ℹ️ Zona reverse {reverse_zone} já existe.")
    else:
        # 2. Cria ficheiro de zona reverse
        soa = f"""$TTL    86400
@   IN  SOA ns1.{fqdn} admin.{fqdn} (
            2024052801 ; Serial
            3600       ; Refresh
            1800       ; Retry
            604800     ; Expire
            86400 )    ; Minimum

    IN  NS  ns1.{fqdn}
"""
        with open(zone_file, "w") as f:
            f.write(soa)
        print(f"✅ Ficheiro de zona reverse criado: {zone_file}")

        # 3. Adiciona zona ao named.conf
        with open(NAMED_CONF, "a") as f:
            f.write(f"""
zone "{reverse_zone}" IN {{
    type master;
    file "{reverse_zone}.zone";
}};
""")
        print(f"✅ Zona reverse adicionada ao {NAMED_CONF}")

    # 4. Adiciona registo PTR
    ptr_host = ip.split('.')[-1]
    ptr_reg = f"{ptr_host}    IN    PTR    {fqdn}\n"
    with open(zone_file, "a") as f:
        f.write(ptr_reg)
    print(f"✅ Registo PTR adicionado: {ptr_reg.strip()}")

    # 5. Reload do serviço DNS
    subprocess.run(["systemctl", "reload", "named"], check=True)
    print("🔄 Servidor DNS recarregado.")

def eliminar_reverse_zone():
    zonas = listar_reverse_zones()
    if not zonas:
        print("⚠️ Não existem zonas reverse para eliminar.")
        return
    zona = input("\n🗑️ Indique a zona reverse a eliminar (exatamente como aparece acima): ").strip()
    if zona not in zonas:
        print(f"❌ A zona '{zona}' não existe!")
        return

    # Remover bloco da zona do named.conf
    with open(NAMED_CONF, "r") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.strip().startswith(f'zone "{zona}"'):
            skip = True
        if not skip:
            new_lines.append(line)
        if skip and line.strip().endswith("};"):
            skip = False
    with open(NAMED_CONF, "w") as f:
        f.writelines(new_lines)
    print(f"🗑️ Zona reverse removida do {NAMED_CONF}")

    # Remover ficheiro de zona
    zone_file = os.path.join(ZONEDIR, f"{zona}.zone")
    if os.path.exists(zone_file):
        os.remove(zone_file)
        print(f"🗑️ Ficheiro de zona removido: {zone_file}")

    # Reload do serviço DNS
    subprocess.run(["systemctl", "reload", "named"], check=True)
    print("🔄 Servidor DNS recarregado.")

def menu():
    while True:
        print("\n===== GESTOR DE ZONAS REVERSE DNS =====")
        print("1️⃣  Adicionar zona reverse")
        print("2️⃣  Remover zona reverse")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            criar_reverse_zone()
        elif escolha == '2':
            eliminar_reverse_zone()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--auto":
        criar_reverse_zone(sys.argv[2])
    else:
        # menu normal
        menu()