#ejecuta el nb 
#DATOS METEO
#DESCARGA Y GUARDA LOS DATOS METEO EN DDB
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

notebook_name=pato_meteo_data
report_name=$notebook_name.$current_time.md
echo "Report: " "$report_name"

report_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/jupyter nbconvert --to markdown --execute --no-input --output $report_path $notebook_path

####################
#DATOS CALAIR
#DESCARGA Y GUARDA LOS DATOS DE CALIDAD EN DDB

notebook_name=pato_calair_data
report_name=$notebook_name.$current_time.md
echo "Report: " "$report_name"

report_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/jupyter nbconvert --to markdown --execute --no-input --output $report_path $notebook_path

####################
#precipitaciones2
echo "precipitaciones2"
/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/codigo/codespaces-jupyter_dam_01/src/write_plotly.py
cp /home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/index.html /var/www/html/meteo/index.html

#temperaturas
echo "temperaturas"
/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/codigo/codespaces-jupyter_dam_01/src/write_plotly_temp.py
cp /home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/temperaturas.html /var/www/html/meteo/temperaturas.html

#####################################

notebook_name=pato_meteo_plotly_report
report_name=meteo.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
cp $report_path /var/www/html/meteo/$report_name


#precipitaciones
notebook_name=pato_precipitaciones_html
report_name=precipitaciones.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/codigo/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
cp $report_path /var/www/html/meteo/$report_name


#general, escribe directamente en var-wwww
echo "general"
/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/codigo/codespaces-jupyter_dam_01/src/write_plotly_general.py

echo "ozono"
/home/jcaubin/codigo/codespaces-jupyter_dam_01/.env/bin/python /home/jcaubin/codigo/codespaces-jupyter_dam_01/src/write_plotly_ozono.py


