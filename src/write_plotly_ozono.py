#grafica de temperaturas

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import duckdb


def main():
        magnitud=14
        with duckdb.connect('/home/jcaubin/datos/duck_test.db') as conn:
                parametro_nombre = conn.sql(f"""
                        SELECT DISTINCT PARAMETRO
                        FROM duck_test.main.CALAIR
                        WHERE MAGNITUD = {magnitud}
                        """).fetchone()[0]
                df = conn.sql(f"""
                        select TS, dia,  h, estacion_desc,valor 
                        from v_CALAIR 
                        where magnitud = {magnitud}
                        and validez = 'V'
                        and date_diff ('hour',TS, current_localtimestamp()) < (25)
                        order by  TS, estacion_desc
                """).df()      
                fig = px.box(df, x= 'TS', y = 'VALOR', title = f'Distribución diaria - {parametro_nombre}', hover_name='ESTACION_DESC',  
                        color_discrete_sequence=["#8484A7"], template='plotly_dark')
                fig.add_hline(y=120, line_dash='dash', line_color='red', annotation_text='límite media 8 h', annotation_position='top right', line_width=1)
                fig.add_hline(y=180, line_dash='dash', line_color='red', annotation_text='aviso', annotation_position='top right', line_width=1)
                fig.add_hline(y=240, line_dash='dash', line_color='red', annotation_text='alerta', annotation_position='top right', line_width=1)

                df = conn.sql(f"""
                        select TS, dia,  h, estacion_desc,valor 
                        from v_CALAIR 
                        where magnitud = {magnitud}
                        and validez = 'V'
                        and date_diff ('hour',TS, current_localtimestamp()) < (7*24)+1
                        order by  TS, estacion_desc
                """).df()   
                fig2 = px.box(df, x= 'TS', y = 'VALOR', title = f'Distribución semanal - {parametro_nombre}', hover_name='ESTACION_DESC',  
                        color_discrete_sequence=["#8484A7"], template='plotly_dark')
                fig2.add_hline(y=120, line_dash='dash', line_color='red', annotation_text='límite media 8 h', annotation_position='top right', line_width=1)
                fig2.add_hline(y=180, line_dash='dash', line_color='red', annotation_text='aviso', annotation_position='top right', line_width=1)
                fig2.add_hline(y=240, line_dash='dash', line_color='red', annotation_text='alerta', annotation_position='top right', line_width=1)


        plotly_jinja_data = {
                "fig":fig.to_html(full_html=False, include_plotlyjs=False , default_width='100%'), 
                "date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S '),
                "title": f"Magnitud {parametro_nombre}",
                "fig2":fig2.to_html(full_html=False, include_plotlyjs=False, default_width='100%'),
                }

        environment = Environment(loader=FileSystemLoader("/home/jcaubin/codigo/codespaces-jupyter_dam_01/templates/"))
        template = environment.get_template("plotly.html")
        output_html_path="/var/www/html/meteo/ozono.html"
        with open(output_html_path, "w", encoding="utf-8") as output_file:
                output_file.write(template.render(plotly_jinja_data))

if __name__=='__main__' :
        main()