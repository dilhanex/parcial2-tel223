# Código de apoyo · Versión A · Reservas de equipos

Material adicional para las Partes 3 y 4. El procedimiento sigue siendo el del enunciado de la Versión A: aquí solo está el código listo para copiar.

## Parte 3 · Tabla

Pegar **al final** de `base/db/01_schema.sql`:

```sql
CREATE TABLE reserva (
  id_reserva SERIAL PRIMARY KEY,
  id_est     INTEGER NOT NULL REFERENCES estudiante,
  id_equipo  INTEGER NOT NULL REFERENCES equipo,
  fecha      DATE NOT NULL,
  dias       INTEGER NOT NULL DEFAULT 1 CHECK (dias BETWEEN 1 AND 7)
);
```

Pegar **al final** de `base/db/02_datos.sql`, reemplazando `<Nombre> <Apellido>` y `<ap>` por los propios:

```sql
INSERT INTO estudiante (nombre, correo, carrera) VALUES ('<Nombre> <Apellido>', '<ap>@ucb.edu.bo', 'INT');
INSERT INTO reserva (id_est, id_equipo, fecha, dias) VALUES (4, 4, '2026-11-30', 2), (1, 5, '2026-12-01', 1);
```

Luego aplicar y verificar como indica el enunciado (`docker compose down -v && docker compose up -d --build`).

## Parte 4 · Rutas

Pegar **al final** de `base/api/main.py`:

```python
# ---------- Versión A: reservas de equipos ----------
COL_RES = "id_reserva AS id, id_est, id_equipo, fecha, dias"


class ReservaNueva(BaseModel):
    id_est: int
    id_equipo: int
    fecha: str
    dias: int = 1


@app.get("/reservas")
def listar_reservas():
    with conectar() as con:
        return con.execute(f"SELECT {COL_RES} FROM reserva ORDER BY id_reserva").fetchall()


@app.get("/estudiantes/{id}/reservas")
def reservas_de_estudiante(id: int):
    with conectar() as con:
        if con.execute("SELECT 1 FROM estudiante WHERE id_est = %s", (id,)).fetchone() is None:
            error(404, "no_existe", f"El estudiante {id} no existe")
        return con.execute(f"SELECT {COL_RES} FROM reserva WHERE id_est = %s ORDER BY fecha", (id,)).fetchall()


@app.post("/reservas", status_code=201)
def crear_reserva(datos: ReservaNueva):
    try:
        with conectar() as con:
            return con.execute(
                f"INSERT INTO reserva (id_est, id_equipo, fecha, dias) VALUES (%s, %s, %s, %s) RETURNING {COL_RES}",
                (datos.id_est, datos.id_equipo, datos.fecha, datos.dias)).fetchone()
    except errors.ForeignKeyViolation:
        error(422, "referencia_inexistente", "El estudiante o el equipo no existe")
    except errors.CheckViolation:
        error(400, "dias_invalidos", "La reserva debe ser de 1 a 7 días")
```

Luego reconstruir como indica el enunciado (`docker compose up -d --build api`) y continuar con la Parte 5.
