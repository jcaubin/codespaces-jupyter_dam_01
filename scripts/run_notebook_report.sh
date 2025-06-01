#ejecuta el nb 

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

notebook_name=pato_meteo_data
report_name=$notebook_name.$current_time.md
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to markdown --execute --no-input --output $report_path $notebook_path

####################

notebook_name=pato_calair_data
report_name=$notebook_name.$current_time.md
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to markdown --execute --no-input --output $report_path $notebook_path

####################
#precipitaciones2
echo "precipitaciones2"
/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/python /home/jcaubin/code/codespaces-jupyter_dam_01/src/write_plotly.py
sudo cp /home/jcaubin/code/codespaces-jupyter_dam_01/reports/index.html /var/www/html/index.html

#temperaturas
echo "temperaturas"
/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/python /home/jcaubin/code/codespaces-jupyter_dam_01/src/write_plotly_temp.py
sudo cp /home/jcaubin/code/codespaces-jupyter_dam_01/reports/temperaturas.html /var/www/html/temperaturas.html

#####################################

notebook_name=pato_meteo_plotly_report
report_name=meteo.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
sudo cp $report_path /var/www/html/$report_name


#precipitaciones
notebook_name=pato_precipitaciones_html
report_name=precipitaciones.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
sudo cp $report_path /var/www/html/$report_name

