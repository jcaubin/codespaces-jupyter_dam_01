#LANZADERA  PARA EJECUTAR NOTEBOOKS Y GENERAR INFORMES EN HTML Y MARKDOWN

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

#SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/jcaubin/codigo/codespaces-jupyter_dam_01"
VENV_PYTHON="${PROJECT_ROOT}/.env/bin/python"

########################################
# DESCARGA Y GUARDA LOS DATOS METEO Y CALAIR EN DDB USANDO UN SCRIPT DE PYTHON
echo "descarga y guarda los datos meteo y calair en ddb"
echo "ejecutando script: ${VENV_PYTHON}  ${PROJECT_ROOT}/src/pato_calair_data.py"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/pato_calair_data.py"

#######################################
#INFORMES HTML
echo "INFORMES DE MAGNITUDES"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/write_plotly_magnitud.py"

#precipitaciones2
echo "precipitaciones"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/write_plotly.py"


########################################
# DESCARGA Y GUARDA LOS DATOS PORTUS
echo "descarga y guarda los datos portus en ddb"
echo "ejecutando script: ${VENV_PYTHON}  ${PROJECT_ROOT}/src/portus_data.py"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/portus_data.py"


