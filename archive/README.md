# Archive Media Stack 🗂️

A privacy-conscious, containerized stack for managing media archives with enhanced security. This setup isolates download-capable containers through a VPN layer (Gluetun) while maintaining full access to Jellyfin and Jellyseerr through the local network.

---

## 🔐 Key Features

- 🌐 **VPN routing with Gluetun** (WireGuard)
- 🔄 **Download-capable containers isolated** by `network_mode: service:gluetun`
- 📦 Services for media organization (Radarr, Sonarr, Prowlarr)
- 📺 Local streaming via **Jellyfin** and **Jellyseerr**
- 🧱 All data is persisted via NFS volumes

---

## 🧰 Service Summary

| Service        | Description                               | Port       | Network        |
|----------------|-------------------------------------------|------------|----------------|
| Jellyfin       | Local media streaming server              | `8096`     | `media_net`    |
| Gluetun        | VPN layer (WireGuard)                     | -          | `vpn_net`      |
| qBittorrent    | Torrent client (via Gluetun)              | `8080`     | via `gluetun`  |
| NZBGet         | Usenet queue (via Gluetun)                | `6789`     | via `gluetun`  |
| Prowlarr       | Indexer manager (via Gluetun)             | `9696`     | via `gluetun`  |
| Sonarr         | Series manager (via Gluetun)              | `8989`     | via `gluetun`  |
| Radarr         | Movie manager (via Gluetun)               | `7878`     | via `gluetun`  |
| Jellyseerr     | Media request interface                   | `5055`     | `media_net`    |

> Containers sharing `network_mode: service:gluetun` are **completely isolated from your LAN**, protecting your privacy.

---

## 📁 Directory Layout
```
archive-stack/
├── docker-compose.yml
├── .env (required)
├── volumes (via NFS)
```

---

## 🔐 VPN Configuration
Ensure your `.env` file contains:

```env
WIREGUARD_PRIVATE_KEY=...
COUNTRY_LOCATION=...
COUNTRY_CITY=...
COUNTRY_NUMBER=...
FIREWALL_OUTBOUND_SUBNETS=
```

Gluetun will restrict outbound traffic to only allowed subnets and expose defined ports.

---

## 🌐 Port Access Summary
| Port | Use           | Source Container |
|------|---------------|------------------|
| 8080 | qBittorrent   | via Gluetun      |
| 6789 | NZBGet        | via Gluetun      |
| 8989 | Sonarr        | via Gluetun      |
| 9696 | Prowlarr      | via Gluetun      |
| 7878 | Radarr        | via Gluetun      |
| 8096 | Jellyfin      | Local (media_net)|
| 5055 | Jellyseerr    | Local (media_net)|

---

Then open:
- `http://localhost:8096` for Jellyfin
- `http://localhost:5055` for Jellyseerr

---

## ⚠️ Disclaimer
This stack is designed for **secure self-hosting**. It does not promote or suggest the use of any specific download services.

Use responsibly and ensure you're complying with all applicable laws and terms of service.

---
