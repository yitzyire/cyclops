# Docker Media Stack 📦

This Compose file defines a complete, self-hosted media stack using Docker. It brings together powerful tools like **Jellyfin**, **Sonarr**, **Radarr**, **qBittorrent**, and more — all networked together under a single private bridge, with persistent data managed over NFS.

> Designed for privacy, automation, and observability.

---

## 🔧 Services Overview

| Service       | Description                                 | Port  |
|---------------|---------------------------------------------|-------|
| **Jellyfin**   | Media server for streaming movies/TV       | `8096` |
| **qBittorrent**| Container with download capability         | `8080` |
| **NZBGet**     | Usenet-based container with queue mgmt     | `6789` |
| **Prowlarr**   | Indexer manager, supports both torrent/NZB | `9696` |
| **Sonarr**     | Tracks and organizes TV series             | `8989` |
| **Radarr**     | Tracks and organizes movies                | `7878` |
| **Jellyseerr** | Media request UI tied to Jellyfin         | `5055` |
| **IP Checker** | Flask-based dashboard to monitor all the above | `5000` |

---

## 📁 Folder Structure

```
cyclops/
├── docker-compose.yml       # Defines the entire stack
├── .env                     # Environment variables (PUID, TZ, etc.)
├── ip-checker/              # Custom Flask dashboard
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html
```

---

## 🗂️ Volumes & Persistence
All services are backed by NFS volumes, defined with `driver_opts`, so config and media persist across restarts.

| Volume             | Purpose           |
|--------------------|-------------------|
| `movies`, `series` | Shared media dirs |
| `*_config`         | Container configs |
| `*_cache`, `*_queue` | Service cache/storage |

Ensure your `.env` has a valid `NFS_SERVER_IP` for this to function correctly.

---

## 🧠 Internal Networking
All services run on a shared `media_net` bridge so they can communicate with each other by container name — no exposed ports required for inter-service APIs.

Example:
```env
JELLYFIN_API_URL=http://jellyfin:8096
```

---

## 🚀 Quickstart

1. **Clone the repo**
```bash
git clone https://github.com/yitzyire/cyclops.git
cd cyclops
```

2. **Set your environment**
```bash
cp .env.example .env
nano .env  # or edit with your preferred editor
```

3. **Bring up the stack**
```bash
docker compose up --build -d
```

4. **Access the dashboard**
Open [http://localhost:5000](http://localhost:5000) for the live Flask dashboard.

---

## ⚠️ Notes
- This stack assumes you have a working NFS server accessible from the host.
- No content is bundled or suggested by default. This stack simply wires up services that can index and manage your **existing media**.

---

## 📜 License
MIT
