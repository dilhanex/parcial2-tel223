# Código de apoyo · Versión B · Incidencias de equipos

Material adicional para las Partes 3 y 4. El procedimiento sigue siendo el del enunciado de la Versión B: aquí solo está el código listo para copiar.

## Parte 3 · Tabla

Pegar **al final** de `base/db/01_schema.sql`:

```sql
CREATE TABLE incidencia (
  id_incid    SERIAL PRIMARY KEY,
  id_equipo   INTEGER NOT NULL REFERENCES equipo,
  descripcion VARCHAR(200) NOT NULL,
  gravedad    VARCHAR(10) NOT NULL DEFAULT 'baja' CHECK (gravedad IN ('baja', 'media', 'alta')),
  fecha       DATE NOT NULL DEFAULT CURRENT_DATE
);
```

Pegar **al final** de `base/db/02_datos.sql`, reemplazando `<Nombre> <Apellido>` y `<ap>` por los propios:

```sql
INSERT INTO estudiante (nombre, correo, carrera) VALUES ('<Nombre> <Apellido>', '<ap>@ucb.edu.bo', 'INT');
INSERT INTO incidencia (id_equipo, descripcion, gravedad) VALUES
  (2, 'Puerto 3 no enciende (reportado por <Apellido>)', 'media'),
  (4, 'Lámpara con poco brillo (reportado por <Apellido>)', 'baja');
```

Luego aplicar y verificar como indica el enunciado (`docker compose down -v && docker compose up -d --build`).

## Parte 4 · Rutas

Pegar **al final** de `base/api/main.py`:

```python
# ---------- Versión B: incidencias de equipos ----------
COL_INC = "id_incid AS id, id_equipo, descripcion, gravedad, fecha"


class IncidenciaNueva(BaseModel):
    id_equipo: int
    descripcion: str
    gravedad: str = "baja"


@app.get("/incidencias")
def listar_incidencias():
    with conectar() as con:
        return con.execute(f"SELECT {COL_INC} FROM incidencia ORDER BY id_incid").fetchall()


@app.get("/equipos/{id}/incidencias")
def incidencias_de_equipo(id: int):
    with conectar() as con:
        if con.execute("SELECT 1 FROM equipo WHERE id_equipo = %s", (id,)).fetchone() is None:
            error(404, "no_existe", f"El equipo {id} no existe")
        return con.execute(f"SELECT {COL_INC} FROM incidencia WHERE id_equipo = %s ORDER BY fecha", (id,)).fetchall()


@app.post("/incidencias", status_code=201)
def crear_incidencia(datos: IncidenciaNueva):
    try:
        with conectar() as con:
            return con.execute(
                f"INSERT INTO incidencia (id_equipo, descripcion, gravedad) VALUES (%s, %s, %s) RETURNING {COL_INC}",
                (datos.id_equipo, datos.descripcion, datos.gravedad)).fetchone()
    except errors.ForeignKeyViolation:
        error(422, "referencia_inexistente", f"El equipo {datos.id_equipo} no existe")
    except errors.CheckViolation:
        error(400, "gravedad_invalida", "La gravedad debe ser baja, media o alta")
```

Luego reconstruir como indica el enunciado (`docker compose up -d --build api`) y continuar con la Parte 5.
