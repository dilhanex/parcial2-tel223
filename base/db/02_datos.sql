-- Segundo Parcial · Datos de prueba
INSERT INTO categoria (nombre) VALUES ('Redes'), ('Multimedia'), ('Cómputo');

INSERT INTO estudiante (nombre, correo, carrera) VALUES
  ('Ana Rojas',   'ana.rojas@ucb.edu.bo',   'INT'),
  ('Luis Poma',   'luis.poma@ucb.edu.bo',   'IMU'),
  ('Sara Quispe', 'sara.quispe@ucb.edu.bo', 'INT');

INSERT INTO equipo (nombre, id_categ) VALUES
  ('Router 1', 1), ('Switch 2', 1), ('Cámara 1', 2), ('Proyector 1', 2), ('Laptop 3', 3);

INSERT INTO prestamo (id_est, id_equipo, estado) VALUES
  (1, 1, 'activo'),
  (2, 3, 'devuelto'),
  (1, 2, 'activo');
