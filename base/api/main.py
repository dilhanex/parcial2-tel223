import os

import psycopg
from psycopg import errors
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

load_dotenv()
DB = os.environ["DATABASE_URL"]
AUTOR = os.environ.get("AUTOR", "sin-apellido")   # viene de APELLIDO en el .env

app = FastAPI(title="Préstamos del laboratorio · Segundo Parcial", root_path="/api")

# El contrato no cambia: misma ruta, mismos campos. Solo cambia dónde se guardan los datos.
COLUMNAS = "id_prest AS id, id_est, id_equipo, estado, fecha_salida"


def conectar():
    return psycopg.connect(DB, row_factory=dict_row)


def error(codigo, nombre, mensaje):
    raise HTTPException(status_code=codigo, detail={"error": nombre, "mensaje": mensaje})


class PrestamoNuevo(BaseModel):
    id_est: int
    id_equipo: int


class CambioEstado(BaseModel):
    estado: str


@app.get("/salud")
def salud():
    with conectar() as con:
        con.execute("SELECT 1")
    return {"estado": "ok", "autor": AUTOR, "db": "ok"}


@app.get("/prestamos")
def listar(estado: str | None = None):
    with conectar() as con:
        if estado:
            return con.execute(f"SELECT {COLUMNAS} FROM prestamo WHERE estado = %s ORDER BY id_prest",
                               (estado,)).fetchall()
        return con.execute(f"SELECT {COLUMNAS} FROM prestamo ORDER BY id_prest").fetchall()


@app.get("/prestamos/{id}")
def consultar(id: int):
    with conectar() as con:
        fila = con.execute(f"SELECT {COLUMNAS} FROM prestamo WHERE id_prest = %s", (id,)).fetchone()
    if fila is None:
        error(404, "no_existe", f"El préstamo {id} no existe")
    return fila


@app.post("/prestamos", status_code=201)
def crear(datos: PrestamoNuevo, response: Response):
    try:
        with conectar() as con:
            nuevo = con.execute(
                f"INSERT INTO prestamo (id_est, id_equipo) VALUES (%s, %s) RETURNING {COLUMNAS}",
                (datos.id_est, datos.id_equipo)).fetchone()
    except errors.ForeignKeyViolation:          # el motor no encontró al estudiante o al equipo
        error(422, "referencia_inexistente", "El estudiante o el equipo no existe")
    except errors.UniqueViolation:              # el equipo ya tiene un préstamo activo
        error(409, "equipo_prestado", f"El equipo {datos.id_equipo} ya está prestado")
    response.headers["Location"] = f"/api/prestamos/{nuevo['id']}"
    return nuevo


@app.patch("/prestamos/{id}")
def cambiar_estado(id: int, datos: CambioEstado):
    try:
        with conectar() as con:
            fila = con.execute(f"UPDATE prestamo SET estado = %s WHERE id_prest = %s RETURNING {COLUMNAS}",
                               (datos.estado, id)).fetchone()
    except errors.CheckViolation:               # estado distinto de activo o devuelto
        error(400, "estado_invalido", "El estado debe ser activo o devuelto")
    except errors.UniqueViolation:              # reactivar un préstamo de un equipo ya prestado
        error(409, "equipo_prestado", "El equipo ya tiene otro préstamo activo")
    if fila is None:
        error(404, "no_existe", f"El préstamo {id} no existe")
    return fila


@app.delete("/prestamos/{id}", status_code=204)
def eliminar(id: int):
    with conectar() as con:
        borradas = con.execute("DELETE FROM prestamo WHERE id_prest = %s", (id,)).rowcount
    if borradas == 0:
        error(404, "no_existe", f"El préstamo {id} no existe")


@app.get("/equipos/disponibles")
def disponibles():
    # La disponibilidad no se guarda: se calcula
    with conectar() as con:
        return con.execute("""
            SELECT q.id_equipo, q.nombre, c.nombre AS categoria
              FROM equipo q JOIN categoria c ON c.id_categ = q.id_categ
             WHERE NOT EXISTS (SELECT 1 FROM prestamo p
                                WHERE p.id_equipo = q.id_equipo AND p.estado = 'activo')
             ORDER BY q.id_equipo""").fetchall()
