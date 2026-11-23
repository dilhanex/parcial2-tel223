# Segundo Parcial práctico · Versión B · Incidencias de equipos

El laboratorio quiere registrar las **incidencias** (fallas) que se detectan en sus equipos, con su gravedad. Se parte del entorno base (préstamo de equipos), que ya funciona después de la Parte 2.

## Parte 3 · Modificar el esquema (20 puntos)

1. Agregar al final de `base/db/01_schema.sql` la tabla **`incidencia`**:

| Columna | Tipo y reglas |
|---|---|
| `id_incid` | entero autoincremental, clave primaria |
| `id_equipo` | entero, obligatorio, referencia a equipo |
| `descripcion` | texto hasta 200 caracteres, obligatorio |
| `gravedad` | texto hasta 10 caracteres, obligatorio, por defecto 'baja', **solo 'baja', 'media' o 'alta'** |
| `fecha` | fecha, obligatoria, por defecto la de hoy |

2. Agregar al final de `db/02_datos.sql`:

   - Un estudiante con **su propio nombre y apellido** (correo `<ap>@ucb.edu.bo`, carrera `INT`).
   - Dos incidencias: una del equipo 2 y otra del equipo 4. En la descripción de ambas escribir `(reportado por <Apellido>)`.

3. Aplicar el cambio: como el volumen de la base ya existe, los scripts no se vuelven a ejecutar solos. Reiniciar la base desde cero:

```bash
docker compose down -v && docker compose up -d --build
```

4. Verificar:

```bash
docker compose exec db psql -U app -d laboratorio -c '\d incidencia'
docker compose exec db psql -U app -d laboratorio -c 'SELECT * FROM incidencia'
```

## Parte 4 · Extender la interfaz (25 puntos)

En `base/api/main.py`, agregar estas tres operaciones. Mantener el estilo del archivo: consultas con `%s` y errores con la función `error()`.

| Método y ruta | Cuerpo | Respuesta correcta | Errores |
|---|---|---|---|
| `GET /incidencias` | — | 200 · lista de incidencias | — |
| `GET /equipos/{id}/incidencias` | — | 200 · incidencias del equipo | 404 si el equipo no existe |
| `POST /incidencias` | id_equipo, descripcion, gravedad (opcional) | 201 · la incidencia creada | 422 si el equipo no existe · 400 si la gravedad no es baja, media o alta · 422 si falta un campo |

Reconstruir la interfaz y revisar que arrancó:

```bash
docker compose up -d --build api
docker compose logs --tail 20 api
```

## Parte 5 · Pruebas y registros (15 puntos)

Ejecutar cada prueba y anotar en la hoja de respuestas el código **obtenido**. En las pruebas con `...`, usar el mismo comando de P4 cambiando solo el cuerpo (`-d`).

| ID | Prueba | Comando | Esperado |
|---|---|---|---|
| P1 | Listar incidencias | `curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/incidencias` | 200 |
| P2 | Incidencias del equipo 2 | `curl -s http://localhost/api/equipos/2/incidencias` | 200 y su incidencia |
| P3 | Equipo inexistente | `curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/equipos/99/incidencias` | 404 |
| P4 | Registrar una incidencia válida | `curl -i -X POST http://localhost/api/incidencias -H "Content-Type: application/json" -d '{"id_equipo":3,"descripcion":"Lente rayado - <ap>","gravedad":"alta"}'` | 201 |
| P5 | Equipo inexistente | `... -d '{"id_equipo":99,"descripcion":"x"}'` | 422 |
| P6 | Gravedad inválida | `... -d '{"id_equipo":3,"descripcion":"x","gravedad":"urgente"}'` | 400 |
| P7 | Falta la descripción | `... -d '{"id_equipo":3}'` | 422 |

Por último, revisar los registros de la interfaz y anotar en la hoja una línea que muestre una de sus pruebas:

```bash
docker compose logs --tail 15 api
```
