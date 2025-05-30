import os
import subprocess
import re
import sys
from shutil import copy2

ZONEDIR = "/var/named"

def listar_zonas():
    zonas = [f for f in os.listdir(ZONEDIR) if f.endswith("zone")]
    print("\nZonas disponíveis:")
    for i, z in enumerate(zonas):
        print(f"{i+1} - {z}")
    return zonas

def validar_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None

def main(dominiio=None):
    if dominiio is None:
        zonas = listar_zonas()
        idx = int(input("Escolha a zona (número): ").strip()) - 1
        ZONA_FILE = os.path.join(ZONEDIR, zonas[idx])

    # Backup
    copy2(ZONA_FILE, ZONA_FILE + ".bak")

    print("\nTipos de registo disponíveis:")
    print("1 - A")
    print("2 - MX")
    tipo = input("Escolha o tipo de registo (1 ou 2): ").strip()

    if tipo == "1":
        subdominio = input("Nome do subdomínio (ex: www): ").strip()
        ip = input("Endereço IPv4: ").strip()
        if not validar_ip(ip):
            print("❌ IP inválido.")
            return
        registo = f"{subdominio}    IN    A    {ip}\n"
    elif tipo == "2":
        prioridade = input("Prioridade MX (ex: 10): ").strip()
        if not prioridade.isdigit():
            print("❌ Prioridade inválida.")
            return
        mailhost = input("Mail host (ex: mail.exemplo.com.): ").strip()
        if not mailhost.endswith('.'):
            print("❌ O mail host deve terminar com ponto.")
            return
        registo = f"@    IN    MX    {prioridade}    {mailhost}\n"
    else:
        print("❌ Tipo inválido.")
        return

    with open(ZONA_FILE, "a") as f:
        f.write(registo)
    print(f"✅ Registo adicionado ao ficheiro de zona: {ZONA_FILE}")

    # Atualizar serial (SOA)
    with open(ZONA_FILE, "r") as f:
        linhas = f.readlines()
    for i, linha in enumerate(linhas):
        if "SOA" in linha:
            # Serial está na linha seguinte ou na mesma linha
            if re.search(r"\d{10}", linha):
                linhas[i] = re.sub(r"(\d{10})", lambda m: str(int(m.group(1)) + 1), linha)
            elif re.search(r"\d{10}", linhas[i+1]):
                linhas[i+1] = re.sub(r"(\d{10})", lambda m: str(int(m.group(1)) + 1), linhas[i+1])
            break
    with open(ZONA_FILE, "w") as f:
        f.writelines(linhas)
    print("🔄 Serial incrementado.")

    subprocess.run(["systemctl", "reload", "named"], check=True)
    print("🔄 Servidor DNS recarregado.")
    print("✅ Registo DNS criado com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--auto":
        main(sys.argv[3])
    else:
        # menu normal
        main()