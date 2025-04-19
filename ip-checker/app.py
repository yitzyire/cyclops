from flask import Flask, jsonify, render_template, request
import subprocess
import json
import psutil
import socket

app = Flask(__name__)

CONTAINERS = [
    "qbittorrent", "nzbget", "sonarr", "prowlarr", "radarr", "jellyfin", "jellyseerr"
]

@app.route("/")
def index():
    host_ip = socket.gethostbyname(socket.gethostname())
    host_stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "uptime": psutil.boot_time(),
        "pids": len(psutil.pids())
    }
    return render_template("index.html", containers=CONTAINERS, host_ip=host_ip, host_stats=host_stats)

@app.route("/api/logs/<container>")
def logs(container):
    try:
        output = subprocess.check_output(["docker", "logs", "--tail", "100", container])
        return output.decode(errors="ignore")
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/api/geoip/<container>")
def geoip(container):
    try:
        ip = subprocess.check_output(["docker", "exec", container, "wget", "-qO-", "https://ipinfo.io/ip"]).decode().strip()
        result = subprocess.check_output(["curl", "-s", f"https://ipinfo.io/{ip}/json"]).decode()
        return jsonify(json.loads(result))
    except Exception as e:
        return jsonify({"error": str(e), "city": "Unknown", "country": "Unknown", "loc": "0,0"})

@app.route("/api/geo-all")
def geo_all():
    results = []
    for container in CONTAINERS:
        try:
            ip = subprocess.check_output(["docker", "exec", container, "wget", "-qO-", "https://ipinfo.io/ip"]).decode().strip()
            result = subprocess.check_output(["curl", "-s", f"https://ipinfo.io/{ip}/json"]).decode()
            geo = json.loads(result)
            results.append({
                "name": container,
                "ip": ip,
                "city": geo.get("city", "Unknown"),
                "country": geo.get("country", "Unknown"),
                "loc": geo.get("loc", "0,0"),
                "org": geo.get("org", "Unknown")
            })
        except Exception as e:
            results.append({
                "name": container,
                "ip": "N/A",
                "city": "Unknown",
                "country": "Unknown",
                "loc": "0,0",
                "org": str(e)
            })
    return jsonify(results)

@app.route("/api/resources/<container>")
def resources(container):
    try:
        stats = subprocess.check_output([
            "docker", "stats", "--no-stream", "--format",
            r"{{.CPUPerc}},{{.MemPerc}},{{.PIDs}}",
            container
        ])
        cpu, mem, pids = stats.decode().strip().replace('%','').split(',')
        return jsonify({
            "cpu": cpu,
            "memory": mem,
            "pids": pids,
            "uptime": "N/A"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/stats/<container>")
def stats(container):
    try:
        inspect = subprocess.check_output(["docker", "inspect", container])
        data = json.loads(inspect)[0]
        state = data["State"]
        net = data["NetworkSettings"]
        ports = net.get("Ports", {})
        bindings = [f"{p}->{b[0]['HostPort']}" for p, b in ports.items() if b]

        return jsonify({
            "uptime": state["StartedAt"],
            "status": state["Status"],
            "cpu": "N/A",
            "memory": "N/A",
            "ports": ", ".join(bindings)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
