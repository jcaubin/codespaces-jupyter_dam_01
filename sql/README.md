Base de datos duckbd para almacenar los datos de calair y meteo

erDiagram
    MAGNITUDES ||--o{ CALAIR : "MAGNITUD"
    ESTACIONES ||--o{ CALAIR : "ESTACION"
    CALAIR ||--|| V_CALAIR : "vista"

    MAGNITUDES {
        int CODIGO PK
        string PARAMETRO
        string UNIDAD
        int COD_TECNICA
        string TECNICA
    }

    ESTACIONES {
        int CODIGO_CORTO PK
        string ESTACION
        int ALTITUD
        double LONGITUD
        double LATITUD
    }

    CALAIR {
        int PROVINCIA
        int MUNICIPIO
        int ESTACION
        int MAGNITUD
        string PUNTO_MUESTREO
        int ANO
        int MES
        int DIA
        int H
        double VALOR
        string VALIDEZ
        string ESTACION_DESC
        int ALTITUD
        string PARAMETRO
        timestamp FX_DATA
    }
