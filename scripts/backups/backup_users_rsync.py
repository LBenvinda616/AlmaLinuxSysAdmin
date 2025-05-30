import os
import datetime
import subprocess

SRC = "/home/"
DEST = "/backup/users"
LOG = "/backup/rsync_users.log"
DATA = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DEST_INCR = f"{DEST}/incr_{DATA}"
DEST_LAST = f"{DEST}/last"

os.makedirs(DEST, exist_ok=True)

# --link-dest só funciona se o diretório "last" existir
link_dest = []
if os.path.islink(DEST_LAST) or os.path.exists(DEST_LAST):
    link_dest = ["--link-dest=" + DEST_LAST]

cmd = ["rsync", "-av", "--delete"] + link_dest + [SRC, DEST_INCR]
with open(LOG, "a") as logf:
    subprocess.run(cmd, stdout=logf, stderr=logf, check=True)

# Atualiza o link simbólico "last"
if os.path.exists(DEST_LAST) or os.path.islink(DEST_LAST):
    os.remove(DEST_LAST)
os.symlink(DEST_INCR, DEST_LAST)

print(f"Backup incremental das áreas dos utilizadores concluído em: {DEST_INCR}")