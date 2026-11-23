#!/bin/bash
# Descarga las imágenes Docker del parcial desde las Releases de este mismo repositorio y las carga.
set -e
URL=$(git -C "$(dirname "$0")" remote get-url origin | sed 's/\.git$//')
echo "Descargando de $URL/releases ..."
wget -q --show-progress -O /tmp/imagenes.tar.gz "$URL/releases/download/imagenes/imagenes.tar.gz"
docker load -i /tmp/imagenes.tar.gz
docker images
