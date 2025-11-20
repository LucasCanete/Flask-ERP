import subprocess


def is_connected():
    try:
        # Revisa si hay conexión real a internet
        #-W 3 define 3 segundos como el timeout
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def list_networks():
    print("🔍 Buscando redes Wi-Fi...\n")
    result = subprocess.run(
        ["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    networks = []
    for i, line in enumerate(lines):
        if not line:
            continue
        ssid, signal = line.split(":")
        networks.append((ssid, signal))
        print(f"{i+1}. {ssid} ({signal}%)")
    return networks

def connect_to_network(ssid, password):
    print(f"\n🔗 Conectando a '{ssid}'...")
    result = subprocess.run(
        ["/usr/bin/nmcli", "dev", "wifi", "connect", ssid, "password", password],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Conectado correctamente y red guardada para futuros inicios.")
        return True
    else:
        print("❌ Error al conectar:\n", result.stderr)
        return []
