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