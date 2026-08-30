-- Tablas maestras
CREATE TABLE IF NOT EXISTS magnitudes (
    codigo       INTEGER PRIMARY KEY,
    parametro    VARCHAR NOT NULL,
    unidad       VARCHAR,
    cod_tecnica  INTEGER,
    tecnica      VARCHAR
);

CREATE TABLE IF NOT EXISTS estaciones (
    codigo        VARCHAR,
    codigo_corto  INTEGER PRIMARY KEY,
    estacion      VARCHAR NOT NULL,
    direccion     VARCHAR,
    longitud      DOUBLE,
    latitud       DOUBLE,
    altitud       INTEGER
);

-- Tabla de hechos (formato largo: 1 fila por hora)
CREATE TABLE IF NOT EXISTS calair (
    provincia      INTEGER NOT NULL,
    municipio      INTEGER NOT NULL,
    estacion       INTEGER NOT NULL,
    magnitud       INTEGER NOT NULL,
    punto_muestreo VARCHAR NOT NULL,
    ano            INTEGER NOT NULL,
    mes            INTEGER NOT NULL,
    dia            INTEGER NOT NULL,
    h              INTEGER NOT NULL,
    valor          DOUBLE,
    validez        VARCHAR(1),
    estacion_desc  VARCHAR,
    altitud        INTEGER,
    parametro      VARCHAR,
    fx_data        TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (punto_muestreo, ano, mes, dia, h)
);

-- Índices útiles para consultas analíticas
CREATE INDEX IF NOT EXISTS idx_calair_ts
    ON calair (ano, mes, dia, h);

CREATE INDEX IF NOT EXISTS idx_calair_magnitud
    ON calair (magnitud, validez);


 --vistas
CREATE OR REPLACE VIEW v_calair AS
SELECT
    provincia,
    municipio,
    estacion,
    magnitud,
    punto_muestreo,
    ano,
    mes,
    dia,
    h,
    valor,
    validez,
    estacion_desc,
    altitud,
    parametro,
    fx_data,
    make_timestamp(ano, mes, dia, h, 0, 0.0) AS ts
FROM calair;   