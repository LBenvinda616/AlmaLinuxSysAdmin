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
    knock

echo "✅ Pacotes de sistema instalados."

echo "🔧 A instalar bibliotecas Python necessárias..."

# Instalar bibliotecas Python (todas são da biblioteca padrão, mas garantimos o pip)
sudo python3 -m pip install --upgrade pip

# As bibliotecas os, datetime, subprocess, re, shutil, socket, time são todas da biblioteca padrão do Python,
# não é necessário instalar via pip. Apenas garantir que o Python 3 está instalado.

echo "✅ Bibliotecas Python padrão disponíveis."

echo "Instalação concluída!"