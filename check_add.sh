for c in qbittorrent nzbget sonarr prowlarr radarr; do
  echo "$c: $(docker exec -it $c curl -s https://ipinfo.io/ip)"
done
