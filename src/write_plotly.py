import plotly.express as px
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import duckdb

with duckdb.connect('/home/jcaubin/duck_test.db') as conn:
        conn.sql("""
        CREATE OR REPLACE TEMP TABLE precip_total_estacion AS         
        select ano, mes, dia, make_date(ano, cast(mes as int), dia) fecha , estacion,estacion_desc, sum(valor) total
        from v_CALAIR 
        where magnitud = 89 --precipitacion 
        and validez = 'V'
        --and estacion_desc in ['Casa de Campo'] --, 'Juan Carlos I', 'El Pardo','Peñagrande', 'Plaza Elíptica']
        and date_diff ('day',TS, current_date()) < (30)
        group by all
        order by all
        """)

        df = conn.sql("""
        select  fecha 
        ,avg(total) precip_media, max(total) precip_max, min(total) precip_min, median(total) precipt_mediana
        , stddev(total) desviacion, count(total) n
        from precip_total_estacion
        group by all
        order by all
        """).df()

        df2 = conn.sql("""
        select *
        from precip_total_estacion
        """).df()


date = datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
fig = px.bar(df, x="fecha", y="precip_media", title = 'Precipitación media',  template='plotly_dark')
fig2 = px.box(df2, x= 'fecha', y = 'total', title = 'Distribución precipitaciones', hover_name='ESTACION_DESC', template='plotly_dark')
plotly_jinja_data = {
        "fig":fig.to_html(full_html=False, include_plotlyjs=False , default_width='600px'), 
        "fig2":fig2.to_html(full_html=False, include_plotlyjs=False),
        "date" : date,
        "title":"Precipitaciones"
        }

environment = Environment(loader=FileSystemLoader('/home/jcaubin/code/codespaces-jupyter_dam_01/templates/'))
template = environment.get_template("plotly.html")
output_html_path="/home/jcaubin/code/codespaces-jupyter_dam_01/reports/index.html"

with open(output_html_path, "w", encoding="utf-8") as output_file:
        output_file.write(template.render(plotly_jinja_data))

  