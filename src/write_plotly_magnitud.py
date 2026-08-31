#grafica de temperaturas

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import duckdb
from pathlib import Path


OUTPUT_DIR = '/var/www/html/meteo'

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / 'duck_test.db'


def informe_magnitud(magnitud, page_name, limites = []):

        with duckdb.connect(DB_PATH) as conn:
                magnitud_nombre, unidad = conn.sql(f"""
                        SELECT  PARAMETRO, UNIDAD
                        FROM duck_test.main.magnitudes
                        WHERE CODIGO = {magnitud}
                        """).fetchone()
                df = conn.sql(f"""
                        select TS, dia,  h, estacion_desc,valor 
                        from v_CALAIR 
                        where magnitud = {magnitud}
                        and validez = 'V'
                        and date_diff ('hour',TS, current_localtimestamp()) < (25)
                        order by  TS, estacion_desc
                """).df()      
                fig = px.box(df, x= 'TS', y ='VALOR', title = f'Distribución diaria - {magnitud_nombre}', hover_name='ESTACION_DESC',  
                        color_discrete_sequence=["#8484A7"], template='plotly_dark', labels={'VALOR': unidad, 'TS': 'Fecha'})
                df = conn.sql(f"""
                        select TS, dia,  h, estacion_desc,valor 
                        from v_CALAIR 
                        where magnitud = {magnitud}
                        and validez = 'V'
                        and date_diff ('hour',TS, current_localtimestamp()) < (7*24)+1
                        order by  TS, estacion_desc
                """).df()   
                fig2 = px.box(df, x= 'TS', y = 'VALOR', title = f'Distribución semanal - {magnitud_nombre}', hover_name='ESTACION_DESC',  
                        color_discrete_sequence=["#8484A7"], template='plotly_dark', labels={'VALOR': unidad, 'TS': 'Fecha'})
                for limite in limites:
                        fig.add_hline(y=limite, line_dash='dash', line_color='red', annotation_text='', annotation_position='top right', line_width=1)
                        fig2.add_hline(y=limite, line_dash='dash', line_color='red', annotation_text='', annotation_position='top right', line_width=1)   
                
        plotly_jinja_data = {
                "fig":fig.to_html(full_html=False, include_plotlyjs=False , default_width='100%'), 
                "date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S '),
                "title": f"{magnitud_nombre}",
                "fig2":fig2.to_html(full_html=False, include_plotlyjs=False, default_width='100%'),
                }

        environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = environment.get_template("plotly.html")
        output_html_path=f"{OUTPUT_DIR}/{page_name}.html"
        with open(output_html_path, "w", encoding="utf-8") as output_file:
                output_file.write(template.render(plotly_jinja_data))

if __name__=='__main__' :
        informe_magnitud(magnitud=12, page_name='nox', limites=[200])
        informe_magnitud(magnitud=10, page_name='pm10', limites=[50])
        informe_magnitud(magnitud=9, page_name='pm25', limites=[25])
        informe_magnitud(magnitud=14, page_name='ozono', limites=[120, 180, 240]) #ozono
        informe_magnitud(magnitud=88, page_name='radiacion') #radiacion
        informe_magnitud(magnitud=83, page_name='temperaturas') #temperatura
        informe_magnitud(magnitud=86, page_name='humedad') #humedad relativa
        

