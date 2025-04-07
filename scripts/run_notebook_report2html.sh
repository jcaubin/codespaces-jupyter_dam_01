#ejecuta el nb 

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

notebook_name=pato_meteo_plotly_report
report_name=index.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
sudo cp $report_path /var/www/html/index.html

#precipitaciones
notebook_name=pato_precipitaciones_html
report_name=precipitaciones.html
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
sudo cp $report_path /var/www/html/$report_name

