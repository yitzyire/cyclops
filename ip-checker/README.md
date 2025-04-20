# Cyclops 👁️

self-hosted dashboard for monitoring your Docker containers — complete with real-time logs, container stats, geo-location mapping

---

## 🔍 Features

- 🔧 Live container stats (CPU, memory, PIDs, uptime)
- 🌍 Geo IP location with Leaflet maps
- 📜 Last 100 logs per container
- 🖱️ Expandable container views with tabbed info
- 🚀 Docker host resource monitoring

---

## 🐳 Setup

### Prerequisites
- Docker
- Docker Compose (v2+)

### 1. Clone the Repo
```bash
git clone https://github.com/yitzyire/cyclops.git
cd cyclops
```

### 2. Configure Environment
(Optional) Create a `.env` file if you're using `PUID`, `PGID`, or other env vars.

### 3. Start the Stack
```bash
docker compose up --build -d
```
Then open [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure
```
cyclops/
├── docker-compose.yml       # Docker services
├── ip-checker/              # Flask dashboard service
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── README.md
```

---

## 🛠 Tech Stack
- Python + Flask
- Leaflet.js + OpenStreetMap
- Docker CLI via `/var/run/docker.sock`

---

## 🧪 Dev Mode
```bash
cd ip-checker
flask --app app.py run --debug
```
Make sure ports don't conflict with your main stack.

---

## 📸 Screenshots
*(Coming soon — feel free to upload and link here!)*
---

## 💡 Contribute
Pull requests welcome — especially if you want to help add:
- Graphing (Chart.js)
- World map view of all containers
- Prometheus-style historical logging
