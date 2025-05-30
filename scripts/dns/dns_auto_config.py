#!/usr/bin/env python3
import subprocess
import sys
import os

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    print("=== Configuração Automática de servidor DNS ===")
    dominio = input("Introduza o domínio (ex: exemplo.com): ").strip()
    ip = input("Introduza o IP (ex: 192.168.1.10): ").strip()

    # Chama o script de zona master
    print("\n▶️ A criar zona master...")
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "dns/dns_master_zone.py"), "--auto", ip, dominio])

    # Chama o script de zona reverse
    print("\n▶️ A criar zona reverse...")
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "dns/dns_reverse_zone.py"), "--auto", ip, dominio])

    # Chama o script de registos DNS
    print("\n▶️ A criar registos DNS...")
    subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "dns/dns_regs.py"), "--auto", ip, dominio])

    print("\n✅ Configuração automática concluída!")

if __name__ == "__main__":
    main()