# TEL-223 · Segundo Parcial · Componente práctico

Examen individual. Cada estudiante resuelve **una versión (A o B)**, indicada por el docente. Todo se anota en la **hoja de respuestas** impresa.

- [Versión A · Reservas de equipos](version-A.md)
- [Versión B · Incidencias de equipos](version-B.md)

En todo el examen, **`<ap>`** es el apellido propio en minúsculas y sin tildes (por ejemplo, `mamani`).

## Tiempo sugerido (135 minutos)

| Parte | Qué | Puntos | Tiempo |
|---|---|---|---|
| 1 | Máquina virtual desde cero | 15 | 30 min |
| 2 | Docker y entorno base | 15 | 20 min |
| 3 | Modificar el esquema (según versión) | 20 | 25 min |
| 4 | Extender la interfaz (según versión) | 25 | 30 min |
| 5 | Pruebas y registros (según versión) | 15 | 20 min |
| 6 | Preguntas de la hoja de respuestas | 10 | 10 min |

---

## Parte 1 · Máquina virtual (15 puntos)

1. En VirtualBox, crear una VM **Ubuntu Server 24.04** con 4 GB de RAM, 2 procesadores y 20 GB de disco.
2. Adaptador 1 en **NAT**. En *Avanzadas → Reenvío de puertos*, agregar:

| Nombre | Protocolo | Puerto anfitrión | Puerto invitado |
|---|---|---|---|
| ssh | TCP | 2222 | 22 |
| web | TCP | 8080 | 80 |

3. Durante la instalación: nombre del equipo **`srv-<ap>`**, usuario **`<ap>`**, marcar **Install OpenSSH server**.
4. Al terminar, conectarse **desde la terminal de la PC** (así se puede copiar y pegar):

```bash
ssh -p 2222 <ap>@127.0.0.1
hostname        # srv-<ap>
ip -br addr     # enp0s3 con 10.0.2.15
```

Anotar en la hoja de respuestas el nombre del equipo y la dirección.

## Parte 2 · Docker y entorno base (15 puntos)

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
exit                                   # volver a entrar por ssh para que el grupo se aplique

git clone <URL de este repositorio>
cd <nombre del repositorio>
bash cargar-imagenes.sh                # descarga y carga nginx, postgres y python

cd base
cp .env.ejemplo .env
nano .env                              # APELLIDO=<ap>  y  DB_CLAVE=<una clave propia>
docker compose up -d --build
docker compose ps
curl -s http://localhost/api/salud
curl -sI http://localhost/ | grep -i x-estudiante
```

Resultado esperado: tres contenedores `parcial-<ap>-web-1`, `parcial-<ap>-api-1` y `parcial-<ap>-db-1` en *running*; `/api/salud` responde `{"estado":"ok","autor":"<ap>","db":"ok"}`; la cabecera `X-Estudiante: <ap>`.

En el navegador de la PC también se puede abrir http://localhost:8080.

### Si la descarga de imágenes en la VM es lenta

Descargar `imagenes.tar.gz` desde la PC (en el navegador: página del repositorio → **Releases** → *imagenes*) y copiarlo a la VM desde la terminal de la PC:

```bash
scp -P 2222 imagenes.tar.gz <ap>@127.0.0.1:~
```

Luego, en la VM: `docker load -i ~/imagenes.tar.gz`. (Ojo: en `scp` el puerto va con **-P mayúscula**.)

### Cómo copiar y pegar

Trabajar siempre desde la terminal SSH de la PC: ahí se pega con clic derecho o Ctrl+Shift+V (la consola de VirtualBox no permite pegar). Copiar los comandos desde esta página de GitHub (botón de copiar de cada bloque), no desde el PDF: el PDF puede cambiar comillas y sangrías.

## Partes 3, 4 y 5

Según la versión asignada: [Versión A](version-A.md) · [Versión B](version-B.md).

## Controles del docente

Levantar la mano en tres momentos; el docente verifica en la VM y anota la hora en la hoja:

| Control | Cuándo | Qué se muestra |
|---|---|---|
| 1 | Al terminar la Parte 2 | `hostname`, `docker compose ps` y `curl -s http://localhost/api/salud` |
| 2 | Al terminar la Parte 3 | `\d` de la tabla nueva y `SELECT *` con su apellido |
| 3 | Al terminar la Parte 5 | Las pruebas P3, P4 y P6 en vivo |

## Reglas

- Individual. Se pueden usar los apuntes y las guías de los laboratorios.
- No apagar ni borrar la VM hasta que el docente haya revisado todo.
