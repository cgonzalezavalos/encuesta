import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns


#------------------------------------------------------------------------

st.set_page_config(layout='wide',
                   initial_sidebar_state="expanded")    

# Set Page Header
st.header("Resultados Encuesta Nacional de Funcionarios Públicos 2023")
# Set custom CSS for hr element
st.markdown(
    """
        <style>
            hr {
                margin-top: 0.0rem;
                margin-bottom: 0.5rem;
                height: 3px;
                background-color: #333;
                border: none;
            }
        </style>
    """,
    unsafe_allow_html=True,
)
#st.caption(f'Fecha de actualización: _{fecha_actualizacion}_')
# Add horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------

with st.sidebar:
    opcion_visualizacion=st.radio('Ver resultados por',['Sector y Servicio','Comparación entre máximos y mínimos', 'Comparación por sexo','Comparación por rango etario', 'Comparación por años de permanencia en el Estado','Comparación por nivel educativo','Comparación por tipo de contrato','Comparación por estamento','Comparación por declaración de discapacidad','Comparación por declaración de pertenencia a pueblos originarios'])

#--------------------------------------------------------------------------
# función para tener los datos en memoria cache
@st.cache_data
def datos_encuesta():
    df=pd.read_excel('BBDD Todos_rev.xlsx')
    mt_indices=pd.read_excel('Maestros.xlsx',sheet_name='indices')
    mt_servicios=pd.read_excel('Maestros.xlsx',sheet_name='servicios')
    df=pd.merge(df,mt_indices,how='left',on='Indice')
    df=pd.merge(df,mt_servicios,how='left',on='Servicio')
    df=df[df['Resultado']!='Respuentas Insuffientes (<10)']
    return df


df_encuesta=datos_encuesta()

@st.cache_data
def maestro_servicios():
    mt_servicios=pd.read_excel('Maestros.xlsx',sheet_name='servicios')
    return mt_servicios

df_mt_servicios=maestro_servicios()
#-------------------------------------------------------------------------
# Función para seleccionar servicios segun ministerio seleccionado
def select_servicio(df_encuesta, option_1):
    if option_1 == 'Todos':
        unique_servicio = df_encuesta['Servicio'].unique()
    else:
        unique_servicio = df_encuesta.query(f'Sector == "{option_1}"')['Servicio'].unique()
    Servicio = pd.DataFrame({'Servicio': unique_servicio})
    nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
    Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
    #Servicio = Servicio.reset_index(drop=True) # modificacion de funcion
    #Servicio = Servicio['Servicio'].tolist() # modificacion de funcion
    return Servicio
#-------------------------------------------------------------------------

# Definir un diccionario de colores para las categoríasn de minimos y maximos por caracteristicas de comparación
categoria_colors = {
    'Minimo': 'orange',
    'Maximo': 'blue'
}
# Definir un diccionario de colores para las dimensiones asociadas a los indices
dimension_colors ={
    'Actitudes Laborales': '#57AADE',
    'Prácticas de Gestión de Personas': '#DE5757'
}
#--------------------------------------------------------------------------
# configuración gráficos
visible_y_axis=False
#--------------------------------------------------------------------------
# tabla de sectores
unique_sector = df_encuesta['Sector'].unique()
Sector = pd.DataFrame({'Sector': unique_sector})
#nuevo_registro = pd.DataFrame({'Sector': ['Todos']})
#Sector = pd.concat([nuevo_registro, Sector])
Sector = Sector.reset_index(drop=True)
Sector = Sector['Sector'].tolist()

#-------------------------------------------------------------------------
# Promedio todos los sectores x indice
df_todos = df_encuesta[(df_encuesta['Servicio'] == 'Todos') & (df_encuesta['Caracteristica de Comparacion'] =='Todos') & (df_encuesta['Tipo'] =='Indice')]
columnas_drop={'Caracteristica de Comparacion','Valor de la Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_todos=df_todos.drop(columns=columnas_drop)
df_todos['Sector']='Administración Central'

# Prpmedio todos los sectores x indice y genero
df_indicadores_genero=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Genero' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_genero=df_indicadores_genero.drop(columns=columnas_drop)
df_indicadores_genero['Sector']='Administración Central'
df_indicadores_genero.rename(columns={'Valor de la Caracteristica de Comparacion':'Genero'},inplace=True)


# Prpmedio todos los sectores x indice y rango etario
df_indicadores_rango_etario=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Edad' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_rango_etario=df_indicadores_rango_etario.drop(columns=columnas_drop)
df_indicadores_rango_etario['Sector']='Administración Central'
df_indicadores_rango_etario.rename(columns={'Valor de la Caracteristica de Comparacion':'Rango Etario'},inplace=True)

# Prpmedio todos los sectores x indice y años en el estado
df_indicadores_años_estado=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Anos de servicio publico' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_años_estado=df_indicadores_años_estado.drop(columns=columnas_drop)
df_indicadores_años_estado['Sector']='Administración Central'
df_indicadores_años_estado.rename(columns={'Valor de la Caracteristica de Comparacion':'Permanencia en el Estado'},inplace=True)

# Prpmedio todos los sectores x indice y Nivel educativo
df_indicadores_nivel_educativo=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Nivel educativo' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_nivel_educativo=df_indicadores_nivel_educativo.drop(columns=columnas_drop)
df_indicadores_nivel_educativo['Sector']='Administración Central'
df_indicadores_nivel_educativo.rename(columns={'Valor de la Caracteristica de Comparacion':'Nivel educativo'},inplace=True)

# Prpmedio todos los sectores x indice y tipo de contrato
df_indicadores_tipo_contrato=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Tipo de contrato' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_tipo_contrato=df_indicadores_tipo_contrato.drop(columns=columnas_drop)
df_indicadores_tipo_contrato['Sector']='Administración Central'
df_indicadores_tipo_contrato.rename(columns={'Valor de la Caracteristica de Comparacion':'Tipo de contrato'},inplace=True)

# Prpmedio todos los sectores x indice y estamento
df_indicadores_estamento=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Estamento' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_estamento=df_indicadores_estamento.drop(columns=columnas_drop)
df_indicadores_estamento['Sector']='Administración Central'
df_indicadores_estamento.rename(columns={'Valor de la Caracteristica de Comparacion':'Estamento'},inplace=True)

# Prpmedio todos los sectores x indice y discapacidad
df_indicadores_discapacidad=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Situacion de discapacidad' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_discapacidad=df_indicadores_discapacidad.drop(columns=columnas_drop)
df_indicadores_discapacidad['Sector']='Administración Central'
df_indicadores_discapacidad.rename(columns={'Valor de la Caracteristica de Comparacion':'Discapacidad'},inplace=True)

# Prpmedio todos los sectores x indice y pueblos originarios
df_indicadores_pueblos_originarios=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Pertenencia a pueblos originarios' & Tipo=='Indice'")
columnas_drop={'Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_indicadores_pueblos_originarios=df_indicadores_pueblos_originarios.drop(columns=columnas_drop)
df_indicadores_pueblos_originarios['Sector']='Administración Central'
df_indicadores_pueblos_originarios.rename(columns={'Valor de la Caracteristica de Comparacion':'Pueblos originarios'},inplace=True)
#-------------------------------------------------------------------------
#Promedios por Sector

sectores = df_encuesta[df_encuesta['Sector'] != 'Todos']['Sector'].unique()
df_promedios_todos = pd.DataFrame()
for sector in sectores:
    df_promedio_sector = df_encuesta[df_encuesta['Sector'] == sector].groupby('Indice')['Resultado'].mean().reset_index()
    df_promedio_sector['Sector'] = sector
    df_promedios_todos = pd.concat([df_promedios_todos, df_promedio_sector])

df_promedios_todos.reset_index(drop=True, inplace=True)
columnas_drop={'Caracteristica de Comparacion','Valor de la Caracteristica de Comparacion','Indicador','Codificacion','Servicio','Tipo'}
df_promedios=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice'").drop(columns=columnas_drop)
df_promedios_todos=pd.concat([df_promedios_todos, df_promedios])
#df_promedios_todos['Resultado']=np.round(df_promedios_todos['Resultado'],2)

#-------------------------------------------------------------------------
#Promedios por Servicio
Servicios = df_encuesta[df_encuesta['Servicio'] != 'Todos']['Servicio'].unique()
df_promedios_servicios_todos = pd.DataFrame()
for servicio in Servicios:
    df_promedios_servicios = df_encuesta[(df_encuesta['Servicio'] == servicio) & (df_encuesta['Caracteristica de Comparacion'] =='Todos') & (df_encuesta['Tipo'] =='Indice')]
    df_promedios_servicios['Servicio'] = servicio
    df_promedios_servicios_todos = pd.concat([df_promedios_servicios_todos, df_promedios_servicios])

columnas_drop={'Caracteristica de Comparacion','Valor de la Caracteristica de Comparacion','Indicador','Codificacion','Tipo'}
df_promedios_servicios_todos=df_encuesta.query("`Caracteristica de Comparacion`=='Todos' & Tipo=='Indice'").drop(columns=columnas_drop)
df_promedios_servicios_todos=pd.concat([df_promedios_servicios_todos, df_promedios])
#df_promedios_servicios_todos=pd.merge(df_promedios_servicios_todos,df_mt_servicios,on='Servicio',how='left')

#-------------------------------------------------------------------------
# indices=df_encuesta['Indice'].unique()
# Maximo=[]
# Minimo=[]
# Servicio_Maximo=[]
# Servicio_Minimo=[]
# Indice=[]
# for indice in indices:
#     datos_x_indice=df_encuesta.query(f"Servicio!='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice' & Indice=='{indice}' & Resultado!='Respuentas Insuffientes (<10)'")
#     for i in range(datos_x_indice.shape[0]):
#         if i==0:
#             ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
#             ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
#             ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
#         else:
#             if datos_x_indice.iloc[i]['Resultado']>ResultadoMaximo:
#                 ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
#                 ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
#             if datos_x_indice.iloc[i]['Resultado']<ResultadoMinimo:
#                 ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
#                 ServicioMinimo=datos_x_indice.iloc[i]['Servicio']
#     #display(f"El servicio con mayor {indice} es {ServicioMaximo} con {ResultadoMaximo}")
#     #display(f"El servicio con menor {indice} es {ServicioMinimo} con {ResultadoMinimo}")
#     Maximo.append(ResultadoMaximo)
#     Minimo.append(ResultadoMinimo)
#     Servicio_Maximo.append(ServicioMaximo)
#     Servicio_Minimo.append(ServicioMinimo)
#     Indice.append(indice)
# df_max=pd.DataFrame({'Indice':Indice,'Categoria':'Maximo','Resultado':Maximo,'Servicio':Servicio_Maximo})
# df_min=pd.DataFrame({'Indice':Indice,'Categoria':'Minimo','Resultado':Minimo,'Servicio':Servicio_Minimo})
# df_max_min=pd.concat([df_max,df_min])
# df_max_min.sort_values(by=['Indice','Categoria'],inplace=True)
# df_max_min['Row_number'] = np.where(df_max_min.reset_index().index==0,0,df_max_min.reset_index().index*0.5)-0.3
# #df_max_min

def min_max_sector(option_1):
    indices=df_encuesta['Indice'].unique()
    Maximo=[]
    Minimo=[]
    Servicio_Maximo=[]
    Servicio_Minimo=[]
    Indice=[]
    for indice in indices:
        if option_1!='Todos':
            datos_x_indice=df_encuesta.query(f"Sector=='{option_1}' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice' & Indice=='{indice}' & Resultado!='Respuentas Insuffientes (<10)'")
        else:
            datos_x_indice=df_encuesta.query(f"Servicio!='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice' & Indice=='{indice}' & Resultado!='Respuentas Insuffientes (<10)'")
        for i in range(datos_x_indice.shape[0]):
            if i==0:
                ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
                ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
                ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
            else:
                if datos_x_indice.iloc[i]['Resultado']>ResultadoMaximo:
                    ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
                    ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
                if datos_x_indice.iloc[i]['Resultado']<ResultadoMinimo:
                    ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
                    ServicioMinimo=datos_x_indice.iloc[i]['Servicio']
        Maximo.append(ResultadoMaximo)
        Minimo.append(ResultadoMinimo)
        Servicio_Maximo.append(ServicioMaximo)
        Servicio_Minimo.append(ServicioMinimo)
        Indice.append(indice)
    df_max=pd.DataFrame({'Indice':Indice,'Categoria':'Maximo','Resultado':Maximo,'Servicio':Servicio_Maximo})
    df_min=pd.DataFrame({'Indice':Indice,'Categoria':'Minimo','Resultado':Minimo,'Servicio':Servicio_Minimo})
    data_max_min_sector=pd.concat([df_max,df_min])
    data_max_min_sector.sort_values(by=['Indice','Categoria'],inplace=True)
    data_max_min_sector['Row_number'] = np.where(data_max_min_sector.reset_index().index==0,0,data_max_min_sector.reset_index().index*0.5)-0.3
    return data_max_min_sector



#-------------------------------------------------------------------------

def indicadores_min_max(option_1):
    data_indicadores=df_encuesta.query(f"Sector=='{option_1}' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indicador' & Resultado!='Respuentas Insuffientes (<10)'")
    data_indicadores_min = data_indicadores.sort_values(by=['Resultado'], ascending=True).head(10)
    data_indicadores_max = data_indicadores.sort_values(by=['Resultado'], ascending=False).head(10)
    data_indicadores_min['Categoria']='Minimo'
    data_indicadores_max['Categoria']='Maximo'
    data_indicadores_min_max=pd.concat([data_indicadores_min,data_indicadores_max])
    return data_indicadores_min_max


#-------------------------------------------------------------------------




if opcion_visualizacion!='Comparación entre máximos y mínimos':
    visualizacion_filtro_servicos=False
else:
    visualizacion_filtro_servicos=True
  
with st.container(): # container de visualizacion de filtros
      col1,col2=st.columns(2,gap="large")
      with col1:
          option_1 = st.selectbox('Sector',Sector)
      with col2:
          option_2 = st.selectbox('Servicio',select_servicio(df_encuesta,option_1),disabled=visualizacion_filtro_servicos)

#-------------------------------------------------------------------------

# aplicar filtros a df_resumen_indicadores
if option_1=='Todos' and option_2=='Todos': #1
     version_grafico='version_1'
     df_promedios_todos=df_promedios_todos.query("Sector=='Todos'")

if option_1!='Todos' and option_2=='Todos':
    version_grafico='version_3'
    df_promedios_todos=df_promedios_todos.query(f"Sector=='{option_1}'")
    df_promedios_todos=pd.concat([df_promedios_todos,df_todos])
    df_promedios_servicios_todos=df_promedios_servicios_todos.query(f"Sector=='{option_1}'")

if option_1!='Todos' and option_2!='Todos':
    version_grafico='version_2'
    df_promedios_todos=df_promedios_todos.query(f"Sector=='{option_1}'")
    df_promedios_servicios_todos=df_promedios_servicios_todos.query(f"Servicio=='{option_2}'")
    df_promedio_servicio=df_promedios_servicios_todos.drop(columns='Sector')
    df_promedio_servicio.rename(columns={'Servicio': 'Sector'}, inplace=True)
    df_promedios_todos=pd.concat([df_promedios_todos,df_todos,df_promedio_servicio])

if option_1=='Todos' and option_2!='Todos':
    version_grafico='version_2'
    df_promedios_servicios_todos=df_promedios_servicios_todos.query(f"Servicio=='{option_2}'")
     
if opcion_visualizacion=='Comparación entre máximos y mínimos' and option_1!='Todos':
    df_max_min=min_max_sector(option_1)
    paso=1
else:
    df_max_min=min_max_sector(option_1)
    paso=2

# with st.container():
#     col1,col2,col3=st.columns(3)
#     with col1:
#         st.dataframe(df_promedios_todos)
#     with col2:
#         st.dataframe(df_todos)
#-------------------------------------------------------------------------


#------------------------------------------------------------------------
# grafico 1
# gráfico general de resultados por indices
if version_grafico=='version_1':
    graf1=px.bar(df_promedios_todos,x='Indice',y='Resultado',title=f'<b>Resultados {option_1} por Indices</b>',color_discrete_map=dimension_colors).\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                 update_xaxes(title_text=None)
if version_grafico=='version_2':
    # graf1=px.bar(df_promedios_servicios_todos,x='Indice',y='Resultado',title=f'<b>Resultados {option_2} por Indices</b>',color_discrete_map=dimension_colors).\
    graf1=px.bar(df_promedios_todos,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices entre todos los sectores y {option_1}</b>',color='Sector', barmode='group',text='Resultado').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                 update_xaxes(title_text=None)
if version_grafico=='version_3':
    graf1=px.bar(df_promedios_todos,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices entre todos los sectores y {option_1}</b>',color='Sector', barmode='group',text='Resultado').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                 update_xaxes(title_text=None)
    #,color='Sector', barmode='group'

#graf1.update_layout(yaxis_tickformat='.0f',width=1300,  # Ancho del gráfico en píxeles
#    height=800,)

graf1.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    yaxis_tickformat='.0f',
    legend=dict(font=dict(size=14)),
    title='',
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1800,  # Ancho del gráfico en píxeles
    height=1300,  # Altura del gráfico en píxeles
)

# Mostrar los valores sobre las barras
#graf1.update_traces(text=graf1.data[0]['y'], texttemplate='%{text:.0f}', textposition='outside')


#---------------------------------------------------------------------------------------
# grafico 2
# Definir un diccionario de colores para las categorías
categoria_colors = {
    'Minimo': 'orange',
    'Maximo': 'blue'
}
# Crear una lista de colores basada en la paleta definida en category_colors
colors = [categoria_colors[c] for c in df_max_min['Categoria'].unique()]

# Crear el gráfico con Plotly Express
graf2 = px.bar(df_max_min, y='Indice', x='Resultado', color='Categoria', color_discrete_map=categoria_colors,title='<b>Servicios con mayor y menor resultado por indice</b>')

# Personalizar el gráfico

graf2.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

graf2.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),
    title='',
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1800,  # Ancho del gráfico en píxeles
    height=1300,  # Altura del gráfico en píxeles
)

## Agregar etiquetas

y_shift = 0  # Variable para ajustar la posición vertical de las anotaciones
for index, row in df_max_min.iterrows():
    
    # Agregar etiqueta
    graf2.add_annotation(
        #x=row['Resultado'], y=row['Row_number'], text=row['Servicio'],
        x=100, y=row['Row_number'], text=row['Servicio'],
        font=dict(size=14, color=categoria_colors[row['Categoria']]),
        showarrow=False,
        xshift=300,
        yshift=y_shift,  # Ajuste vertical
    )
    
    y_shift -= 0.01  # Cambio en la posición vertical para la próxima anotación
#---------------------------------------------------------------------------------------
# grafico 3

graf3=px.bar(df_indicadores_genero,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y género en la administración central</b>',color='Genero', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf3.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)
#---------------------------------------------------------------------------------------
# grafico 4

graf4=px.bar(df_indicadores_rango_etario,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y rango etario en la administración central</b>',color='Rango Etario', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf4.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)

#---------------------------------------------------------------------------------------

# grafico 5

graf5=px.bar(df_indicadores_años_estado,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y años de permanencia en la administración central</b>',color='Permanencia en el Estado', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf5.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)
#---------------------------------------------------------------------------------------

# grafico 6

graf6=px.bar(df_indicadores_nivel_educativo,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y nivel educativo</b>',color='Nivel educativo', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf6.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)

#---------------------------------------------------------------------------------------

# grafico 7

graf7=px.bar(df_indicadores_tipo_contrato,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y tipo de contrato</b>',color='Tipo de contrato', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf7.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)
#---------------------------------------------------------------------------------------

# grafico 8

graf8=px.bar(df_indicadores_estamento,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y estamento</b>',color='Estamento', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf8.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)
#---------------------------------------------------------------------------------------

# grafico 9

graf9=px.bar(df_indicadores_discapacidad,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y declaración de discapacidad</b>',color='Discapacidad', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf9.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)
#---------------------------------------------------------------------------------------

# grafico 9

graf10=px.bar(df_indicadores_pueblos_originarios,x='Indice',y='Resultado',title=f'<b>Comparación de resultados por indices y pertenencia a pueblos originarios</b>',color='Pueblos originarios', barmode='group',text='Resultado').\
    update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf10.update_layout(
    yaxis=dict(title='', tickfont=dict(size=14)),
    xaxis=dict(title='Resultado', tickfont=dict(size=14)),
    legend=dict(font=dict(size=14)),#location='top right'),
    showlegend=True,
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,
    width=1300,  # Ancho del gráfico en píxeles
    height=800,  # Altura del gráfico en píxeles
)

#---------------------------------------------------------------------------------------
# grafico 11
df_indicadores_min_max=indicadores_min_max(option_1).sort_values(by=['Categoria','Resultado'],ascending=[False,True])
# Crear una lista de colores basada en la paleta definida en category_colors
colors = [categoria_colors[c] for c in df_indicadores_min_max['Categoria'].unique()]
# Crear el gráfico con Plotly Express
graf11 = px.bar(df_indicadores_min_max, y='Indicador', x='Resultado', color='Categoria' ,title='<b>Servicios con mayor y menor resultado por indicador</b>') #,

# # Personalizar el gráfico
# graf11.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)

# graf11.update_layout(
#     yaxis=dict(title='', tickfont=dict(size=14)),
#     xaxis=dict(title='Resultado', tickfont=dict(size=14)),
#     legend=dict(font=dict(size=14)),
#     title='',
#     showlegend=True,
#     barmode='group',
#     bargap=0.15,
#     bargroupgap=0.1,
#     width=1400,  # Ancho del gráfico en píxeles
#     height=1000,  # Altura del gráfico en píxeles
# )

# ## Agregar etiquetas
# y_shift = 0  # Variable para ajustar la posición vertical de las anotaciones
# for index, row in df_indicadores_min_max.iterrows():
    
#     # Agregar etiqueta
#     graf11.add_annotation(
#         x=100, y=row['Row_number'], text=row['Servicio'],
#         font=dict(size=14, color=categoria_colors[row['Categoria']]),
#         showarrow=False,
#         xshift=300,
#         yshift=y_shift,  # Ajuste vertical
#     )
    
#     y_shift -= 0.01  # Cambio en la posición vertical para la próxima anotación
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

if opcion_visualizacion=='Sector y Servicio':
    st.plotly_chart(graf1)
    # st.dataframe(df_promedios_todos)
    # st.dataframe(df_promedios_servicios_todos)
if opcion_visualizacion=='Comparación entre máximos y mínimos':
    with st.container():
        if option_1=="Todos":
            st.markdown(f'<h3>Comparación de resultados por indices entre servicios públicos de todos los sectores</h3>', unsafe_allow_html=True)
        else: 
            st.markdown(f'<h3>Comparación de resultados por indices entre servicios públicos del {option_1}</h3>', unsafe_allow_html=True)
        st.plotly_chart(graf2)
    with st.container():
        if option_1=="Todos":
            st.markdown(f'<h3>Comparación de resultados de indicadores con mejores y peores resultados entre servicios públicos de todos los sectores</h3>', unsafe_allow_html=True)
        else: 
            st.markdown(f'<h3>Comparación de resultados de indicadores con mejores y peores resultados entre servicios públicos del {option_1}</h3>', unsafe_allow_html=True)
        st.plotly_chart(graf11)
if opcion_visualizacion=='Comparación por sexo':
    st.plotly_chart(graf3)
    #st.dataframe(df_indicadores_genero)
if opcion_visualizacion=='Comparación por rango etario':
    st.plotly_chart(graf4)
    #st.dataframe(df_indicadores_rango_etario)
if opcion_visualizacion=='Comparación por años de permanencia en el Estado':
    st.plotly_chart(graf5)
    #st.dataframe(df_indicadores_años_estado)
if opcion_visualizacion=='Comparación por nivel educativo':
    st.plotly_chart(graf6)
if opcion_visualizacion=='Comparación por tipo de contrato':
    st.plotly_chart(graf7)
if opcion_visualizacion=='Comparación por estamento':
    st.plotly_chart(graf8)
if opcion_visualizacion=='Comparación por declaración de discapacidad':
    st.plotly_chart(graf9)
if opcion_visualizacion=='Comparación por declaración de pertenencia a pueblos originarios':
    st.plotly_chart(graf10)
#Pertenencia a pueblos originarios
