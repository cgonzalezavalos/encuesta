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
@st.cache_data
def datos_encuesta():
    df=pd.read_excel('BBDD Todos_rev.xlsx')
    mt_indices=pd.read_excel('Maestros.xlsx',sheet_name='indices')
    mt_servicios=pd.read_excel('Maestros.xlsx',sheet_name='servicios')

    df=pd.merge(df,mt_indices,how='left',on='Indice')
    df=pd.merge(df,mt_servicios,how='left',on='Servicio')
    return df


df_encuesta=datos_encuesta()

#-------------------------------------------------------------------------
# data frame con resumen de indicadores
df_resumen_indicaores=df_encuesta.query("`Servicio`=='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice'") #`Indice` == 'Satisfaccion Laboral' & 

#-------------------------------------------------------------------------
# Definir un diccionario de colores para las categorías
categoria_colors = {
    'Minimo': 'orange',
    'Maximo': 'blue'
}

dimension_colors ={
    'Actitudes Laborales': '#57AADE',
    'Prácticas de Gestión de Personas': '#DE5757'
}

#--------------------------------------------------------------------------
# configuración gráficos
visible_y_axis=False
#--------------------------------------------------------------------------
#st.dataframe(df_resumen_indicaores)


#-------------------------------------------------------------------------
# gráfico Convocatorias por Año
graf1=px.bar(df_resumen_indicaores,x='Indice',y='Resultado',title='<b>Resultados por Indices</b>',color_discrete_sequence=[dimension_colors]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
graf1.update_layout(yaxis_tickformat='.0f')

st.plotly_chart(graf1)
