import pandas as pd
import numpy as np

def datos_encuesta():
    df=pd.read_excel('C:/Users/cgonzaleza/Desktop/python/encuesta/BBDD Todos_rev.xlsx')
    mt_indices=pd.read_excel('C:/Users/cgonzaleza/Desktop/python/encuesta/Maestros.xlsx',sheet_name='indices')
    mt_servicios=pd.read_excel('C:/Users/cgonzaleza/Desktop/python/encuesta/Maestros.xlsx',sheet_name='servicios')
    df=pd.merge(df,mt_indices,how='left',on='Indice')
    df=pd.merge(df,mt_servicios,how='left',on='Servicio')
    df=df[df['Resultado']!='Respuentas Insuffientes (<10)']
    return df
df_encuesta=datos_encuesta()

option_1='Ministerio de Salud'

indices=df_encuesta['Indice'].unique()
Maximo=[]
Minimo=[]
Servicio_Maximo=[]
Servicio_Minimo=[]
Indice=[]
for indice in indices:
    if option_1!='Todos':
        datos_x_indice=df_encuesta.query(f"Sector=='{option_1}' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice' & Indice=='{indice}' & Resultado!='Respuentas Insuffientes (<10)'")
        print('datos_x_indice')
        print('-'*100)
        print(datos_x_indice)
        print('-'*100)
    else:
        datos_x_indice=df_encuesta.query(f"Servicio!='Todos' & `Caracteristica de Comparacion`=='Todos' & Tipo=='Indice' & Indice=='{indice}' & Resultado!='Respuentas Insuffientes (<10)'")
    for i in range(datos_x_indice.shape[0]):
        print(datos_x_indice.iloc[i])
        print('+'*100)
        if i==0:
            ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
            ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
            ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
            ServicioMinimo=datos_x_indice.iloc[i]['Servicio']
            print('*'*100)
            print('ResultadoMaximo: ',ResultadoMaximo)
            print('ServicioMaximo: ',ServicioMaximo)
            print('ResultadoMinimo: ',ResultadoMinimo)
            print('ServicioMinimo: ',ServicioMinimo)
        else:
            print(datos_x_indice.iloc[i]['Resultado'])
            if datos_x_indice.iloc[i]['Resultado']>ResultadoMaximo:
                ResultadoMaximo=datos_x_indice.iloc[i]['Resultado']
                ServicioMaximo=datos_x_indice.iloc[i]['Servicio']
                print('*'*100)
                print(ResultadoMaximo)
                print(ServicioMaximo)
            if datos_x_indice.iloc[i]['Resultado']<=ResultadoMinimo:
                ResultadoMinimo=datos_x_indice.iloc[i]['Resultado']
                ServicioMinimo=datos_x_indice.iloc[i]['Servicio']
                print('*'*100)
                print(ResultadoMinimo)
                print(ServicioMinimo)
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

print(data_max_min_sector)