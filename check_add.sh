for c in qbittorrent nzbget sonarr prowlarr; do
  echo "$c: $(docker exec -it $c curl -s https://ipinfo.io/ip)"
done
