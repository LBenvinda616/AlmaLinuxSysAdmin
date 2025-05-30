#!/usr/bin/env python3
import subprocess
import os

KNOCKD_CONF = "/etc/knockd.conf"

def pedir_sequencia():
    seq = input("Introduza a sequência de portas para abrir o SSH (ex: 1234,2345,3456): ").strip()
    portas = [p.strip() for p in seq.split(",") if p.strip().isdigit()]
    if len(portas) < 2:
        print("❌ Tem de indicar pelo menos duas portas.")
        exit(1)
    return portas

def configurar_knockd(portas):
    print("🔧 A configurar knockd para port knocking SSH...")
    conf = f"""
[options]
    logfile = /var/log/knockd.log

[abrir-ssh]
    sequence    = {','.join(portas)}
    seq_timeout = 10
    command     = /usr/bin/firewall-cmd --add-port=22/tcp --permanent; /usr/bin/firewall-cmd --reload
    tcpflags    = syn

[fechar-ssh]
    sequence    = {','.join(reversed(portas))}
    seq_timeout = 10
    command     = /usr/bin/firewall-cmd --remove-port=22/tcp --permanent; /usr/bin/firewall-cmd --reload
    tcpflags    = syn
"""
    with open(KNOCKD_CONF, "w") as f:
        f.write(conf.strip() + "\n")
    print(f"✅ Configuração escrita em {KNOCKD_CONF}")

def ativar_knockd():
    print("🔄 Ativando e iniciando knockd...")
    sysconfig = "/etc/sysconfig/knockd"
    if os.path.exists(sysconfig):
        with open(sysconfig, "r") as f:
            linhas = f.readlines()
        with open(sysconfig, "w") as f:
            found = False
            for linha in linhas:
                if linha.startswith("OPTIONS="):
                    f.write('OPTIONS="-i any"\n')
                    found = True
                else:
                    f.write(linha)
            if not found:
                f.write('OPTIONS="-i any"\n')
    subprocess.run(["systemctl", "enable", "--now", "knockd"], check=True)
    print("✅ knockd ativo e a escutar.")

def main():
    if os.geteuid() != 0:
        print("⚠️ Este script deve ser executado como root (sudo).")
        exit(1)
    portas = pedir_sequencia()
    configurar_knockd(portas)
    ativar_knockd()
    print("\n🌟 Port knocking configurado! Use a sequência para abrir o SSH.")

if __name__ == "__main__":
    main()