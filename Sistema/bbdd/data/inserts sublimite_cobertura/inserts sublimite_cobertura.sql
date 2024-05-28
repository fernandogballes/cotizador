-- inserts sublimites RC Explotacion, RC Post-trabajos
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Explotacion', 'RC Post-trabajos')
WHERE sublimite.sublimite IN ('150000', '300000', '600000', '1000000', '2000000', '3000000', '4000000', '6000000', '8000000', '10000000');

-- inserts sublimites RC Accidentes de trabajo, RC Subsidiaria
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Accidentes de trabajo', 'RC Subsidiaria')
WHERE sublimite.sublimite IN ('150000', '300000', '600000', '750000');

-- inserts sublimites RC Trabajos en caliente
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura = 'RC Trabajos en caliente'
WHERE sublimite.sublimite IN ('90000', '150000', '300000', '600000', '1000000', '2000000');

-- inserts sublimites RC Derribos, RC Conducciones
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Derribos', 'RC Conducciones')
WHERE sublimite.sublimite IN ('75000', '150000', '300000', '500000', '1000000', '1500000', '2000000', '3000000', '4000000', '5000000');

-- inserts sublimites RC Locativa y RC Contaminacion accidental
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Locativa', 'RC Contaminacion accidental')
WHERE sublimite.sublimite IN ('90000', '150000', '300000', '600000', '1000000');

-- inserts sublimites RC Danos a las redes de comunicaciones publicas
INSERT INTO sublimite_cobertura (id_sublimite, id_cobertura)
SELECT sublimite.id_sublimite, cobertura.id_cobertura
FROM catalogo_sublimites AS sublimite
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura = 'RC Danos a las redes de comunicaciones publicas'
WHERE sublimite.sublimite IN ('90000', '150000', '300000');
