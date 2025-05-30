#!/usr/bin/env python3
import socket
import time

def knock(host, ports, delay=0.5):
    print(f"🔑 A enviar knocks para {host} nas portas {ports}...")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect_ex((host, port))
            s.close()
            print(f"  -> Knock na porta {port}")
        except Exception as e:
            print(f"  [!] Erro ao contactar porta {port}: {e}")
        time.sleep(delay)
    print("✅ Sequência de knocks enviada.")

if __name__ == "__main__":
    host = input("Endereço do servidor (ex: 192.168.1.100): ").strip()
    seq = input("Sequência de portas separadas por vírgula (ex: 1234,2345,3456): ").strip()
    ports = [int(p.strip()) for p in seq.split(",") if p.strip().isdigit()]
    delay = input("Delay entre knocks (segundos, default 0.5): ").strip()
    delay = float(delay) if delay else 0.5
    knock(host, ports, delay)
    print("Agora pode tentar ligar por SSH se o servidor estiver configurado para port knocking.")