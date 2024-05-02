import pandas as pd
import numpy as np
import streamlit as st
#import plotly.express as px
#import matplotlib.pyplot as plt
#%matplotlib inline
#import seaborn as sns


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
df=pd.read_excel('BBDD Todos_rev.xlsx')

mt_indices=pd.read_excel('Maestros.xlsx',sheet_name='indices')
mt_servicios=pd.read_excel('Maestros.xlsx',sheet_name='servicios')

df=pd.merge(df,mt_indices,how='left',on='Indices')
df=pd.merge(df,mt_servicios,how='left',on='Servicio')

#-------------------------------------------------------------------------
# data frame con resumen de indicadores
df_resumen_indicaores=df.query("`Servicio`=='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice'") #`Indice` == 'Satisfaccion Laboral' & 

#-------------------------------------------------------------------------
st.dataframe(df_resumen_indicaores)
