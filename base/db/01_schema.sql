-- Segundo Parcial · Tablas del préstamo de equipos
-- Orden: primero las tablas a las que otras apuntan.

CREATE TABLE categoria (
  id_categ  SERIAL PRIMARY KEY,
  nombre    VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE estudiante (
  id_est    SERIAL PRIMARY KEY,
  nombre    VARCHAR(80)  NOT NULL,
  correo    VARCHAR(120) NOT NULL UNIQUE,
  carrera   VARCHAR(3)   NOT NULL CHECK (carrera IN ('INT', 'IMU'))
);

CREATE TABLE equipo (
  id_equipo SERIAL PRIMARY KEY,
  nombre    VARCHAR(60) NOT NULL,
  id_categ  INTEGER NOT NULL REFERENCES categoria
);

CREATE TABLE prestamo (
  id_prest     SERIAL PRIMARY KEY,
  id_est       INTEGER NOT NULL REFERENCES estudiante,
  id_equipo    INTEGER NOT NULL REFERENCES equipo,
  fecha_salida DATE NOT NULL DEFAULT CURRENT_DATE,
  estado       VARCHAR(10) NOT NULL DEFAULT 'activo'
               CHECK (estado IN ('activo', 'devuelto'))
);

-- Un equipo no puede tener dos préstamos activos a la vez.
CREATE UNIQUE INDEX un_activo_por_equipo ON prestamo (id_equipo) WHERE estado = 'activo';
