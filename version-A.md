# Segundo Parcial práctico · Versión A · Reservas de equipos

El laboratorio quiere que los estudiantes **reserven un equipo** para una fecha y por una cantidad de días. Se parte del entorno base (préstamo de equipos), que ya funciona después de la Parte 2.

## Parte 3 · Modificar el esquema (20 puntos)

1. Agregar al final de `base/db/01_schema.sql` la tabla **`reserva`**:

| Columna | Tipo y reglas |
|---|---|
| `id_reserva` | entero autoincremental, clave primaria |
| `id_est` | entero, obligatorio, referencia a estudiante |
| `id_equipo` | entero, obligatorio, referencia a equipo |
| `fecha` | fecha, obligatoria |
| `dias` | entero, obligatorio, por defecto 1, **entre 1 y 7** |

2. Agregar al final de `db/02_datos.sql`:

   - Un estudiante con **su propio nombre y apellido** (correo `<ap>@ucb.edu.bo`, carrera `INT`). Será el estudiante número 4.
   - Dos reservas: una del estudiante 4 (su registro) y otra del estudiante 1.

3. Aplicar el cambio: como el volumen de la base ya existe, los scripts no se vuelven a ejecutar solos. Reiniciar la base desde cero:

```bash
docker compose down -v && docker compose up -d --build
```

4. Verificar:

```bash
docker compose exec db psql -U app -d laboratorio -c '\d reserva'
docker compose exec db psql -U app -d laboratorio -c 'SELECT * FROM reserva'
```

## Parte 4 · Extender la interfaz (25 puntos)

En `base/api/main.py`, agregar estas tres operaciones. Mantener el estilo del archivo: consultas con `%s` y errores con la función `error()`.

| Método y ruta | Cuerpo | Respuesta correcta | Errores |
|---|---|---|---|
| `GET /reservas` | — | 200 · lista de reservas | — |
| `GET /estudiantes/{id}/reservas` | — | 200 · reservas del estudiante | 404 si el estudiante no existe |
| `POST /reservas` | id_est, id_equipo, fecha, dias (opcional) | 201 · la reserva creada | 422 si el estudiante o el equipo no existe · 400 si dias está fuera de 1 a 7 · 422 si falta un campo |

Reconstruir la interfaz y revisar que arrancó:

```bash
docker compose up -d --build api
docker compose logs --tail 20 api
```

## Parte 5 · Pruebas y registros (15 puntos)

Ejecutar cada prueba y anotar en la hoja de respuestas el código **obtenido**. En las pruebas con `...`, usar el mismo comando de P4 cambiando solo el cuerpo (`-d`).

| ID | Prueba | Comando | Esperado |
|---|---|---|---|
| P1 | Listar reservas | `curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/reservas` | 200 |
| P2 | Reservas del estudiante 4 (usted) | `curl -s http://localhost/api/estudiantes/4/reservas` | 200 y su reserva |
| P3 | Estudiante inexistente | `curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/estudiantes/99/reservas` | 404 |
| P4 | Registrar una reserva válida | `curl -i -X POST http://localhost/api/reservas -H "Content-Type: application/json" -d '{"id_est":4,"id_equipo":5,"fecha":"2026-12-02","dias":3}'` | 201 |
| P5 | Equipo inexistente | `... -d '{"id_est":4,"id_equipo":99,"fecha":"2026-12-02"}'` | 422 |
| P6 | Días fuera de rango | `... -d '{"id_est":4,"id_equipo":5,"fecha":"2026-12-02","dias":9}'` | 400 |
| P7 | Falta la fecha | `... -d '{"id_est":4,"id_equipo":5}'` | 422 |

Por último, revisar los registros de la interfaz y anotar en la hoja una línea que muestre una de sus pruebas:

```bash
docker compose logs --tail 15 api
```
