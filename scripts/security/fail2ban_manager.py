#!/usr/bin/env python3
import subprocess
import os
import sys

JAIL_LOCAL = "/etc/fail2ban/jail.local"

def instalar_fail2ban():
    print("🔧 A instalar fail2ban...")
    subprocess.run(["sudo", "dnf", "install", "-y", "fail2ban"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "--now", "fail2ban"], check=True)
    print("✅ fail2ban instalado e ativo.")

def configurar_ssh():
    print("🔧 A configurar fail2ban para SSH...")
    config = """
[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
maxretry = 5
bantime = 3600
findtime = 600
"""
    with open(JAIL_LOCAL, "w") as f:
        f.write(config.strip() + "\n")
    subprocess.run(["sudo", "systemctl", "restart", "fail2ban"], check=True)
    print("✅ fail2ban configurado para SSH.")

def listar_ips_bloqueados():
    print("🔎 IPs bloqueados pelo fail2ban (jail sshd):")
    result = subprocess.run(
        ["sudo", "fail2ban-client", "status", "sshd"],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if "Banned IP list:" in line:
            print(line)
            return
    print("Nenhum IP bloqueado.")

def desbloquear_ip():
    ip = input("Introduza o IP a desbloquear: ").strip()
    subprocess.run(["sudo", "fail2ban-client", "set", "sshd", "unbanip", ip], check=True)
    print(f"✅ IP {ip} desbloqueado.")

def menu():
    while True:
        print("\n===== GESTOR FAIL2BAN SSH =====")
        print("1️⃣  Instalar e configurar fail2ban para SSH")
        print("2️⃣  Listar IPs bloqueados")
        print("3️⃣  Desbloquear IP")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            instalar_fail2ban()
            configurar_ssh()
        elif escolha == '2':
            listar_ips_bloqueados()
        elif escolha == '3':
            desbloquear_ip()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ Este script deve ser executado como root (sudo).")
        sys.exit(1)
    menu()