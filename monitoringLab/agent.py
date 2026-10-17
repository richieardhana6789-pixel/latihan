import psutil
import requests
import time
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
SERVER_IP = "192.168.238.X" # Ganti dengan IP Server Debian 13 Anda

@app.route('/agent/command', methods=['POST'])
def execute_command():
    data = request.json
    action = data.get('action')
    if action == 'restart':
        os.system("shutdown /r /t 5")
        return jsonify({"status": "restarting"})
    elif action == 'shutdown':
        os.system("shutdown /s /t 5")
        return jsonify({"status": "shutting down"})
    return jsonify({"status": "invalid action"}), 400

def send_heartbeat():
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            # Simulasi atau ambil suhu jika sensor tersedia
            payload = {
                "name": os. 컴퓨터name if os.name == 'nt' else "PC-Client",
                "status": "online",
                "cpu": cpu,
                "ram": ram,
                "temp": 45  # Dummy / ambil dari sensor hardware
            }
            requests.post(f"http://{SERVER_IP}/api/heartbeat", json=payload, timeout=2)
        except Exception as e:
            print("Gagal kirim heartbeat:", e)
        time.sleep(5)

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=send_heartbeat, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)