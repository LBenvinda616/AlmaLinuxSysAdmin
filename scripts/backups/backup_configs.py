import os
import datetime
import subprocess

DESTINO = "/backup/configs"
DATA = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ARQUIVO = f"{DESTINO}/backup_configs_{DATA}.tar.gz"

os.makedirs(DESTINO, exist_ok=True)

files = ["/etc/passwd", "/etc/shadow", "/etc/group", "/etc/gshadow", "/etc/sudoers"]

cmd = ["tar", "czvf", ARQUIVO] + files
subprocess.run(cmd, check=True)

print(f"Backup dos ficheiros críticos criado em: {ARQUIVO}")