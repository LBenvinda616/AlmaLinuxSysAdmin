#!/usr/bin/env python3
import subprocess
import os
import sys

# Caminho base onde estão os scripts
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "scripts/"))

MENUS = {
    "Gestão DNS": {
        "Configuração Automática DNS": os.path.join(SCRIPTS_DIR, "dns/dns_auto_config.py"),
        "Gerir zonas master": os.path.join(SCRIPTS_DIR, "dns/dns_master_zone.py"),
        "Gerir registos": os.path.join(SCRIPTS_DIR, "dns/dns_regs.py"),
        "Gerir zonas reverse": os.path.join(SCRIPTS_DIR, "dns/dns_reverse_zone.py"),
    },
    "Gestão de VirtualHosts Apache": {
        "Gerir VirtualHosts": os.path.join(SCRIPTS_DIR, "dns/vhosts.py"),
    },
    "Gestão de Samba": {
        "Gestor de partilhas Samba": os.path.join(SCRIPTS_DIR, "samba/samba_manager.py"),
    },
    "Gestão de NFS": {
        "Gestor de partilhas NFS": os.path.join(SCRIPTS_DIR, "nfs/nfs_manager.py"),
    },
    "Gestão de RAID": {
        "Criar RAID 5": os.path.join(SCRIPTS_DIR, "raid/raid5_setup.py"),
    },
    "Backups": {
        "Backup configs críticos": os.path.join(SCRIPTS_DIR, "backups/backup_configs.py"),
        "Backup incremental utilizadores": os.path.join(SCRIPTS_DIR, "backups/backup_users_rsync.py"),
    },
    "Segurança": {
        "Gestor fail2ban": os.path.join(SCRIPTS_DIR, "security/fail2ban_manager.py"),
        "Configurar port knocking (servidor)": os.path.join(SCRIPTS_DIR, "security/ssh_host_knock_config.py"),
        "Port knocking (cliente)": os.path.join(SCRIPTS_DIR, "security/ssh_client_knock_config.py"),
    }
}

def escolher_opcao(opcoes):
    for i, nome in enumerate(opcoes, 1):
        print(f"{i} - {nome}")
    print("0 - Voltar")
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "0":
        return None
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(opcoes):
            return opcoes[idx]
    except ValueError:
        pass
    print("❌ Opção inválida.")
    return None

def main():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        temas = list(MENUS.keys())
        tema = escolher_opcao(temas)
        if tema is None:
            print("👋 A sair...")
            break
        while True:
            print(f"\n--- {tema} ---")
            scripts = list(MENUS[tema].keys())
            script_nome = escolher_opcao(scripts)
            if script_nome is None:
                break
            script_path = MENUS[tema][script_nome]
            if not os.path.exists(script_path):
                print(f"❌ Script não encontrado: {script_path}")
                continue
            print(f"▶️ A executar: {script_nome}\n")
            try:
                subprocess.run(["python3", script_path])
            except Exception as e:
                print(f"❌ Erro ao executar o script: {e}")

if __name__ == "__main__":
    main()