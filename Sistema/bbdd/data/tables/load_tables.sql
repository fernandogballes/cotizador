CREATE TABLE catalogo_provincias(
    id_provincia SERIAL PRIMARY KEY,
    provincia varchar(50)
);

CREATE TABLE clientes (
    id_cliente varchar(9) PRIMARY KEY,
    nombre_cliente varchar(250) UNIQUE NOT NULL,
    volumen_facturacion FLOAT NOT NULL,
    id_provincia INT NOT NULL,
    FOREIGN KEY (id_provincia) REFERENCES catalogo_provincias(id_provincia)
);

CREATE TABLE catalogo_actividades (
    id_actividad SERIAL PRIMARY KEY,
    nombre_actividad varchar(100) UNIQUE NOT NULL,
    agravada_flag BOOLEAN NOT NULL
);

CREATE TABLE catalogo_coberturas (
    id_cobertura SERIAL PRIMARY KEY,
    nombre_cobertura varchar(100) UNIQUE NOT NULL
);

CREATE TABLE ofertas (
    id_oferta SERIAL PRIMARY KEY,
    id_cliente varchar(100) NOT NULL,
    suma_asegurada FLOAT NOT NULL,
    limite_anualidad FLOAT NOT NULL,
    semaforo INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE catalogo_franquicias (
    id_franquicia SERIAL PRIMARY KEY,
    franquicia varchar(100) NOT NULL
);

CREATE TABLE catalogo_sublimites (
    id_sublimite SERIAL PRIMARY KEY,
    sublimite varchar(100) NOT NULL
);

CREATE TABLE actividad_cliente (
    id_cliente varchar(100) NOT NULL,
    id_actividad INT NOT NULL,
    id_oferta INT NOT NULL,
    PRIMARY KEY (id_cliente, id_actividad, id_oferta),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_actividad) REFERENCES catalogo_actividades(id_actividad),
    FOREIGN KEY (id_oferta) REFERENCES ofertas(id_oferta)
);

CREATE TABLE actividad_cobertura (
    id_actividad INT NOT NULL,
    id_cobertura INT NOT NULL,
    PRIMARY KEY (id_actividad, id_cobertura),
    FOREIGN KEY (id_actividad) REFERENCES catalogo_actividades(id_actividad),
    FOREIGN KEY (id_cobertura) REFERENCES catalogo_coberturas(id_cobertura)
);

CREATE TABLE oferta_cobertura (
    id_oferta INT NOT NULL,
    id_cobertura INT NOT NULL,
    id_franquicia INT NOT NULL,
    id_sublimite INT NOT NULL,
    PRIMARY KEY (id_oferta, id_cobertura),
    FOREIGN KEY (id_cobertura) REFERENCES catalogo_coberturas(id_cobertura),
    FOREIGN KEY (id_oferta) REFERENCES ofertas(id_oferta),
    FOREIGN KEY (id_franquicia) REFERENCES catalogo_franquicias(id_franquicia),
    FOREIGN KEY (id_sublimite) REFERENCES catalogo_sublimites(id_sublimite)
);

CREATE TABLE franquicia_cobertura (
	id_franquicia INT NOT NULL,
	id_cobertura INT NOT NULL,
    PRIMARY KEY (id_franquicia, id_cobertura),
    FOREIGN KEY (id_cobertura) REFERENCES catalogo_coberturas(id_cobertura),
    FOREIGN KEY (id_franquicia) REFERENCES catalogo_franquicias(id_franquicia)	
);

CREATE TABLE sublimite_cobertura (
	id_sublimite INT NOT NULL,
	id_cobertura INT NOT NULL,
    PRIMARY KEY (id_sublimite, id_cobertura),
    FOREIGN KEY (id_cobertura) REFERENCES catalogo_coberturas(id_cobertura),
    FOREIGN KEY (id_sublimite) REFERENCES catalogo_sublimites(id_sublimite)	
);
