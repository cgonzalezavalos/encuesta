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
#-------------------------------------------------------------------------
# Función para seleccionar servicios segun ministerio seleccionado
def select_servicio(df_encuesta, option_2):
    if option_2 == 'Todos':
        unique_servicio = option_2['Servicio'].unique()
    else:
        unique_servicio = df_encuesta.query(f'Sector == "{option_2}"')['Servicio'].unique()
    Servicio = pd.DataFrame({'Servicio': unique_servicio})
    nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
    Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

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
nuevo_registro = pd.DataFrame({'Sector': ['Todos']})
Sector = pd.concat([nuevo_registro, Sector])
Sector = Sector.reset_index(drop=True)
Sector = Sector['Sector'].tolist()

#-------------------------------------------------------------------------


sectores = df_encuesta[df_encuesta['Sector'] != 'Todos']['Sector'].unique()
df_promedios_todos = pd.DataFrame()
for sector in sectores:
    df_promedio_sector = df_encuesta[df_encuesta['Sector'] == sector].groupby('Indice')['Resultado'].mean().reset_index()
    df_promedio_sector['Sector'] = sector
    df_promedios_todos = pd.concat([df_promedios_todos, df_promedio_sector])

df_promedios_todos.reset_index(drop=True, inplace=True)


columnas_drop={'Caracteristica de Comparacion','Valor de la Caracteristica de Comparacion','Indicador','Codificacion','Dimensión','Servicio','Tipo'}
df_promedios=df_encuesta.query("Servicio=='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice'").drop(columns=columnas_drop)
df_promedios_todos=pd.concat([df_promedios_todos, df_promedios])
#-------------------------------------------------------------------------
indices=df_encuesta['Indice'].unique()
Maximo=[]
Minimo=[]
Servicio_Maximo=[]
Servicio_Minimo=[]
Indice=[]
for indice in indices:
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
    #display(f"El servicio con mayor {indice} es {ServicioMaximo} con {ResultadoMaximo}")
    #display(f"El servicio con menor {indice} es {ServicioMinimo} con {ResultadoMinimo}")
    Maximo.append(ResultadoMaximo)
    Minimo.append(ResultadoMinimo)
    Servicio_Maximo.append(ServicioMaximo)
    Servicio_Minimo.append(ServicioMinimo)
    Indice.append(indice)
df_max=pd.DataFrame({'Indice':Indice,'Categoria':'Maximo','Resultado':Maximo,'Servicio':Servicio_Maximo})
df_min=pd.DataFrame({'Indice':Indice,'Categoria':'Minimo','Resultado':Minimo,'Servicio':Servicio_Minimo})
df_max_min=pd.concat([df_max,df_min])
df_max_min.sort_values(by=['Indice','Categoria'],inplace=True)
df_max_min['Row_number'] = np.where(df_max_min.reset_index().index==0,0,df_max_min.reset_index().index*0.5)-0.3
#df_max_min

#-------------------------------------------------------------------------

with st.container():
            col1,col2=st.columns(2,gap="large")
            with col1:
                option_1 = st.selectbox('Sector',Sector)
            with col2:
                option_2 = st.selectbox('Servicio',select_servicio(df_encuesta,option_1))




#-------------------------------------------------------------------------
# aplicar filtros a df_resumen_indicadores
if option_1=='Todos': #1
     df_promedios_todos=df_promedios_todos.query("Sector=='Todos'")
else:
    df_promedios_todos=df_promedios_todos.query(f"Sector=='{option_1}'")
#     # data frame con resumen de indicadores
#     df_resumen_indicaores=df_encuesta[(df_encuesta.Servicio==option_2) & (df_encuesta['Caracteristica de Comparacion']=='Todos') & (df_encuesta['Tipo']=='Indice')]
# if option_1!='Todos' and option_2=='Todos':
     
#st.dataframe(df_promedios_todos)
#-------------------------------------------------------------------------


#------------------------------------------------------------------------
# gráfico general de resultados por indices
graf1=px.bar(df_promedios_todos,x='Indice',y='Resultado',title=f'<b>Resultados {option_1} por Indices</b>').update_yaxes(visible=visible_y_axis,title_text=None).\
                 update_xaxes(title_text=None)
graf1.update_layout(yaxis_tickformat='.0f',width=1000,  # Ancho del gráfico en píxeles
    height=800,)

#------------------------------------------------------------------------
# Definir un diccionario de colores para las categorías
categoria_colors = {
    'Minimo': 'orange',
    'Maximo': 'blue'
}
# Crear una lista de colores basada en la paleta definida en category_colors
colors = [categoria_colors[c] for c in df_max_min['Categoria'].unique()]

#sns.barplot(y='Indice', x='Resultado', data=df_max_min,hue='Categoria',palette=colors)

# graf2=sns.barplot(y='Indice', x='Resultado', data=df_max_min,hue='Categoria',palette=colors)
# graf2.yaxis.set_tick_params(labelsize=14)
# graf2.xaxis.set_tick_params(labelsize=14)
# graf2.set_ylabel('')
# graf2.set_xlabel('')

# graf2.figure.set_figheight(15)
# graf2.figure.set_figwidth(20)

# # Agregar etiquetas
# for index, row in df_max_min.iterrows():
#     graf2.annotate(row['Servicio'],
#                  #xy=(0,row['Row_number']),
#                  xy=(100,row['Row_number']),
#                  xytext=(15,0),
#                  textcoords='offset points',
#                  fontsize=18,
#                  color=categoria_colors[row['Categoria']],)  # Color basado en la categoría
# graf2.legend(bbox_to_anchor=(0, 1.05),fontsize=14)
# # Eliminar las líneas de enmarcado
# graf2.spines['top'].set_visible(False)
# graf2.spines['right'].set_visible(False)
# graf2.spines['bottom'].set_visible(True)
# graf2.spines['left'].set_visible(True)


# Crear el gráfico con Plotly Express
graf2 = px.bar(df_max_min, y='Indice', x='Resultado', color='Categoria', color_discrete_map=categoria_colors)

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

# Agregar etiquetas
y_shift = 0  # Variable para ajustar la posición vertical de las anotaciones
for index, row in df_max_min.iterrows():
    graf2.add_annotation(
        x=row['Resultado'], y=row['Indice'], text=row['Servicio'],
        font=dict(size=14, color=categoria_colors[row['Categoria']]),
        showarrow=False,
        xshift=100,
        yshift=y_shift,  # Ajuste vertical
    )
    y_shift -= 1  # Cambio en la posición vertical para la próxima anotación



st.plotly_chart(graf1)
st.plotly_chart(graf2)
#st.pyplot(graf2.figure)




