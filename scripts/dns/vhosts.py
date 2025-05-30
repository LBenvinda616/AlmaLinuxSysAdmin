#!/usr/bin/env python3
import os
import subprocess

APACHE_SITES_AVAILABLE = "/etc/httpd/conf.d"
WEB_ROOT = "/var/www"

def listar_dominios():
    confs = [f[:-5] for f in os.listdir(APACHE_SITES_AVAILABLE) if f.endswith('.conf')]
    print("\n🌐 Domínios disponíveis:")
    if confs:
        for d in confs:
            print(f" - {d}")
    else:
        print(" (nenhum domínio configurado)")
    return confs

def criar_virtualhost():
    dominios_existentes = listar_dominios()
    dominio = input("\n🌐 Nome do domínio a criar (ex: exemplo.local): ").strip()
    if dominio in dominios_existentes:
        print(f"⚠️ O domínio '{dominio}' já existe!")
        return

    pasta = os.path.join(WEB_ROOT, dominio)
    conf_path = os.path.join(APACHE_SITES_AVAILABLE, f"{dominio}.conf")

    # 1. Criar diretório do site
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"📁 Diretório criado: {pasta}")

    # 2. Criar página de boas-vindas
    index_path = os.path.join(pasta, "index.html")
    with open(index_path, "w") as f:
        f.write(f"""<html>
<head><title>Bem-vindo a {dominio}</title></head>
<body>
    <h1>Bem-vindo ao domínio {dominio}!</h1>
</body>
</html>
""")
    print(f"✅ Página de boas-vindas criada: {index_path}")

    # 3. Criar ficheiro de configuração do VirtualHost
    conf = f"""<VirtualHost *:80>
    ServerName {dominio}
    DocumentRoot {pasta}
    <Directory {pasta}>
        AllowOverride All
        Require all granted
    </Directory>
    ErrorLog /var/log/httpd/{dominio}_error.log
    CustomLog /var/log/httpd/{dominio}_access.log combined
</VirtualHost>
"""
    with open(conf_path, "w") as f:
        f.write(conf)
    print(f"✅ VirtualHost criado: {conf_path}")

    # 4. Adicionar ao /etc/hosts
    hosts_line = f"127.0.0.1\t{dominio}\n"
    with open("/etc/hosts", "r") as f:
        hosts = f.readlines()
    if not any(dominio in line for line in hosts):
        with open("/etc/hosts", "a") as f:
            f.write(hosts_line)
        print(f"📝 Domínio adicionado ao /etc/hosts")

    # 5. Reiniciar Apache
    subprocess.run(["systemctl", "reload", "httpd"], check=True)
    print("🔄 Apache recarregado.")

    print(f"\n🌍 Aceda a http://{dominio} no seu browser!")

def eliminar_virtualhost():
    dominios_existentes = listar_dominios()
    if not dominios_existentes:
        print("⚠️ Não existem domínios para eliminar.")
        return
    dominio = input("\n🗑️ Indique o domínio a eliminar: ").strip()
    if dominio not in dominios_existentes:
        print(f"❌ O domínio '{dominio}' não existe!")
        return

    conf_path = os.path.join(APACHE_SITES_AVAILABLE, f"{dominio}.conf")
    pasta = os.path.join(WEB_ROOT, dominio)

    # Remover ficheiro de configuração
    if os.path.exists(conf_path):
        os.remove(conf_path)
        print(f"🗑️ VirtualHost removido: {conf_path}")

    # Remover pasta do site (opcional, pode comentar se não quiser apagar os ficheiros)
    if os.path.exists(pasta):
        try:
            import shutil
            shutil.rmtree(pasta)
            print(f"🗑️ Pasta do site removida: {pasta}")
        except Exception as e:
            print(f"⚠️ Erro ao remover a pasta do site: {e}")

    # Remover do /etc/hosts
    with open("/etc/hosts", "r") as f:
        hosts = f.readlines()
    hosts_novo = [l for l in hosts if dominio not in l]
    with open("/etc/hosts", "w") as f:
        f.writelines(hosts_novo)
    print(f"🗑️ Entrada removida do /etc/hosts")

    # Reiniciar Apache
    subprocess.run(["systemctl", "reload", "httpd"], check=True)
    print("🔄 Apache recarregado.")

def menu():
    while True:
        print("\n===== GESTOR DE VIRTUALHOSTS APACHE =====")
        print("1️⃣  Adicionar VirtualHost")
        print("2️⃣  Remover VirtualHost")
        print("0️⃣  Sair")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == '1':
            criar_virtualhost()
        elif escolha == '2':
            eliminar_virtualhost()
        elif escolha == '0':
            print("👋 A sair...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()