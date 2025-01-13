#ejecuta el nb 

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

notebook_name=pato_meteo_data
report_name=$notebook_name.$current_time.md
echo "Report: " "$report_name"

report_path=/home/jcaubin/code/github/codespaces-jupyter_dam_01/reports/$report_name 
notebook_path=/home/jcaubin/code/github/codespaces-jupyter_dam_01/notebooks/$notebook_name.ipynb

/home/jcaubin/code/github/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to markdown --execute --no-input --output $report_path $notebook_path
