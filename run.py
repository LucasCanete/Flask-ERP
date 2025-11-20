from erp_system import app
from erp_system.utils.scheduler import start_scheduler
import webbrowser
import threading
import socket


# Obtener IP local automáticamente
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No se envía nada, solo se fuerza a obtener una IP válida
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Abre el navegador en la IP local
def open_browser():
    local_ip = get_local_ip()
    webbrowser.open(f"http://{local_ip}:5000/services/services_view")

if __name__ == '__main__':
   # threading.Timer(1.0, open_browser).start()
    with app.app_context():
        start_scheduler()
    app.run(host="0.0.0.0", port=5000)
