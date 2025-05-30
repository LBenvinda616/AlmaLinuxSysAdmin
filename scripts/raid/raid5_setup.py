#!/usr/bin/env python3
import os
import subprocess

def listar_drives():
    print("=== Dispositivos disponíveis para RAID ===")
    # Lista apenas discos (exclui partições e loop devices)
    result = subprocess.check_output("lsblk -dn -o NAME,SIZE,TYPE | grep disk", shell=True).decode().strip()
    if not result:
        print("Nenhum disco disponível encontrado.")
        return []
    drives = []
    for line in result.splitlines():
        nome, size, tipo = line.split()
        device = f"/dev/{nome}"
        print(f"{device} - {size}")
        drives.append(device)
    return drives

def criar_raid5():
    drives = listar_drives()
    if not drives:
        print("❌ Não há discos disponíveis para RAID.")
        return

    dispositivos = input("Indique os dispositivos para o RAID 5 (ex: /dev/sdb /dev/sdc /dev/sdd): ").strip().split()
    if len(dispositivos) < 3:
        print("❌ RAID 5 requer pelo menos 3 discos.")
        return

    md_device = "/dev/md0"
    ponto_montagem = input("Indique o diretório para montar o RAID (ex: /mnt/raid5): ").strip()

    # Criar RAID 5
    print("🔧 A criar RAID 5...")
    subprocess.run(["mdadm", "--create", md_device, "--level=5", "--raid-devices={}".format(len(dispositivos))] + dispositivos, check=True)
    print(f"✅ RAID 5 criado em {md_device}")

    # Guardar configuração do mdadm
    subprocess.run(["mdadm", "--detail", "--scan"], check=True, stdout=open("/etc/mdadm.conf", "w"))

    # Criar sistema de ficheiros
    print("🔧 A formatar o RAID com ext4...")
    subprocess.run(["mkfs.ext4", "-F", md_device], check=True)

    # Criar diretório de montagem
    os.makedirs(ponto_montagem, exist_ok=True)

    # Obter UUID
    blkid = subprocess.check_output(["blkid", "-s", "UUID", "-o", "value", md_device]).decode().strip()
    fstab_line = f"UUID={blkid} {ponto_montagem} ext4 defaults 0 0\n"

    # Adicionar ao /etc/fstab
    with open("/etc/fstab", "a") as f:
        f.write(fstab_line)

    # Montar
    subprocess.run(["mount", ponto_montagem], check=True)
    print(f"✅ RAID 5 montado em {ponto_montagem}")

    print("\nResumo:")
    print(f"RAID: {md_device}")
    print(f"Montagem: {ponto_montagem}")
    print(f"UUID: {blkid}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ Este script deve ser executado como root (sudo).")
        exit(1)
    criar_raid5()