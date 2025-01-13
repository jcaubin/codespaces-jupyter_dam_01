#ejecuta el nb 

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Current Time : $current_time"

file_name=pato_meteo_madrid
new_fileName=$file_name.$current_time.html
echo "FileName: " "$new_fileName"

report_path=/home/jcaubin/code/github/codespaces-jupyter_dam_01/reports/$new_fileName 
notebook_path=/home/jcaubin/code/github/codespaces-jupyter_dam_01/notebooks/pato_meteo_seaborn.ipynb

/home/jcaubin/code/github/codespaces-jupyter_dam_01/.venv/bin/jupyter nbconvert --to html --execute --no-input --output $report_path $notebook_path
