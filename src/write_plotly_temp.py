#grafica de temperaturas

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import duckdb


def main():
        with duckdb.connect('/home/jcaubin/duck_test.db') as conn:
                df = conn.sql("""
                        select TS, dia,  h, estacion_desc,valor 
                        from v_CALAIR 
                        where magnitud = 83
                        and validez = 'V'
                        and date_diff ('hour',TS, current_localtimestamp()) < (24)
                        order by  TS, estacion_desc
                """).df()


        #pio.templates.default = "plotly_dark"        
        fig = px.box(df, x= 'TS', y = 'VALOR', title = 'Distribución temperaturas2', hover_name='ESTACION_DESC',  color_discrete_sequence=["#8484A7"], template='plotly_dark')

        plotly_jinja_data = {
                "fig":fig.to_html(full_html=False, include_plotlyjs=False , default_width='600px'), 
                "date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S '),
                "title": "Temperaturas"
                }

        environment = Environment(loader=FileSystemLoader("/home/jcaubin/code/codespaces-jupyter_dam_01/templates/"))
        template = environment.get_template("plotly.html")
        output_html_path="/home/jcaubin/code/codespaces-jupyter_dam_01/reports/temperaturas.html"
        with open(output_html_path, "w", encoding="utf-8") as output_file:
                output_file.write(template.render(plotly_jinja_data))

if __name__=='__main__' :
        main()