-- inserts franquicias RC Explotacion, RC Post-trabajos, RC Locativa, RC Contaminacion accidental, RC Danos a las redes de comunicaciones publicas
INSERT INTO franquicia_cobertura (id_franquicia, id_cobertura)
SELECT franquicia.id_franquicia, cobertura.id_cobertura
FROM catalogo_franquicias AS franquicia
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Explotacion', 'RC Post-trabajos', 'RC Locativa', 'RC Contaminacion accidental', 'RC Danos a las redes de comunicaciones publicas')
WHERE franquicia.franquicia IN ('300 a 600', '600 a 1500', '1500 a 3000', '3000 a 6000');

-- inserts franquicias RC Derribos, RC Conducciones, RC Trabajos en caliente
INSERT INTO franquicia_cobertura (id_franquicia, id_cobertura)
SELECT franquicia.id_franquicia, cobertura.id_cobertura
FROM catalogo_franquicias AS franquicia
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Derribos', 'RC Conducciones', 'RC Trabajos en caliente')
WHERE franquicia.franquicia IN ('1500', '10% minimo 1500 maximo 3000', '20% minimo 1500 maximo 3000', '20% minimo 3000 maximo 6000');

-- inserts franquicias RC Subsidiaria, RC Accidentes de trabajo
INSERT INTO franquicia_cobertura (id_franquicia, id_cobertura)
SELECT franquicia.id_franquicia, cobertura.id_cobertura
FROM catalogo_franquicias AS franquicia
JOIN catalogo_coberturas AS cobertura ON cobertura.nombre_cobertura IN ('RC Subsidiaria', 'RC Accidentes de trabajo')
WHERE franquicia.franquicia = 'Sin franquicia';
