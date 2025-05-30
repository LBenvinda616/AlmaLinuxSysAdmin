#!/bin/bash
# filepath: /scripts/install_all_dependencies.sh

echo "🔧 A instalar pacotes de sistema..."

# Ativar EPEL (para AlmaLinux/CentOS)
sudo dnf install -y epel-release
sudo dnf update -y

# Pacotes de sistema necessários
sudo dnf install -y \
    python3 \
    python3-pip \
    bind bind-utils \
    httpd \
    samba cifs-utils \
    nfs-utils \
    rsync tar \
    mdadm \
    fail2ban \
    iptables-services \
    net-tools \
    knock-server

echo "✅ Pacotes de sistema instalados."

# Ativar e iniciar serviços principais
echo "🔄 A ativar e iniciar serviços..."
for svc in named httpd smb nfs-server fail2ban firewalld knockd; do
    if systemctl list-unit-files | grep -q "^${svc}\.service"; then
        sudo systemctl enable --now $svc
        echo "✅ Serviço $svc ativado e iniciado."
    else
        echo "⚠️  Serviço $svc não encontrado, ignorado."
    fi
done

echo "🔧 A instalar bibliotecas Python necessárias..."

# Instalar bibliotecas Python (todas são da biblioteca padrão, mas garantimos o pip)
sudo python3 -m pip install --upgrade pip

# As bibliotecas os, datetime, subprocess, re, shutil, socket, time são todas da biblioteca padrão do Python,
# não é necessário instalar via pip. Apenas garantir que o Python 3 está instalado.

echo "✅ Bibliotecas Python padrão disponíveis."

echo "Instalação concluída!"