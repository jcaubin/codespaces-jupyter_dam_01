#LANZADERA  PARA EJECUTAR NOTEBOOKS Y GENERAR INFORMES EN HTML Y MARKDOWN

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
VENV_PYTHON="${PROJECT_ROOT}/.venv/bin/python"

########################################
# DESCARGA Y GUARDA LOS DATOS METEO Y CALAIR EN DDB USANDO UN SCRIPT DE PYTHON
echo "descarga y guarda los datos meteo y calair en ddb"
echo "ejecutando script: ${VENV_PYTHON}  /home/jcaubin/code/codespaces-jupyter_dam_01/src/pato_calair_data.py"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/pato_calair_data.py"

#######################################
#INFORMES HTML
echo "INFORMES DE MAGNITUDES"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/write_plotly_magnitud.py"

#precipitaciones2
#echo "precipitaciones"
"${VENV_PYTHON}" "${PROJECT_ROOT}/src/write_plotly.py"


#temperaturas
#echo "temperaturas"
#/home/jcaubin/code/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/code/codespaces-jupyter_dam_01/src/write_plotly_temp.py
#cp /home/jcaubin/code/codespaces-jupyter_dam_01/reports/temperaturas.html /var/www/html/meteo/temperaturas.html


#echo "ozono"
#/home/jcaubin/code/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/code/codespaces-jupyter_dam_01/src/write_plotly_ozono.py

#echo "radiacion"
#/home/jcaubin/code/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/code/codespaces-jupyter_dam_01/src/write_plotly_radiacion.py


