-- Trigger function to insert mandatory coverages for a new activity
CREATE OR REPLACE FUNCTION insert_mandatory_coverages()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO actividad_cobertura (id_actividad, id_cobertura)
    VALUES
        (NEW.id_actividad, (SELECT id_cobertura FROM catalogo_coberturas WHERE nombre_cobertura = 'RC Explotacion')),
        (NEW.id_actividad, (SELECT id_cobertura FROM catalogo_coberturas WHERE nombre_cobertura = 'RC Accidentes de trabajo')),
        (NEW.id_actividad, (SELECT id_cobertura FROM catalogo_coberturas WHERE nombre_cobertura = 'RC Post-trabajos'));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function on insert
CREATE TRIGGER after_insert_catalogo_actividades
AFTER INSERT ON catalogo_actividades
FOR EACH ROW
EXECUTE FUNCTION insert_mandatory_coverages();
