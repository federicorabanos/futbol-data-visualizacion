#La sheet en la cual está la tabla es esta --> https://docs.google.com/spreadsheets/d/15CqzJhJH434Fqno_BSV_QVgsixlr2nM93nzDMOncY5k/edit?usp=sharing 
#Los paths a los archivos son propios de cada cpu y directorio.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pygsheets
from datetime import date
from PIL import Image   

equivalenciaNombres = {'Argentinos':'Argentinos Juniors', 
'Velez':'Vélez Sarsfield', 
'Lanus':'Lanús', 
'Central Cba (SdE)': 'Central Córdoba (SdE)', 
'Def y Justicia':'Defensa y Justicia',
'Colon':'Colón',
'Huracan':'Huracán',
'Sarmiento':'Sarmiento (J)',
'Atl Tucuman': 'Atlético Tucumán',
'Gimnasia (LP)': 'Gimnasia y Esgrima (LP)',
'Union': 'Unión',
"Newells": "Newell's Old Boys"}

#Armo driver con selenium para sacar tablas de Promiedos.
options = Options()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://www.promiedos.com.ar/primera') #Se puede usar otro link de otra tabla más vieja de Promiedos.
html = driver.page_source
driver.close()

#Va variando donde colocar la tabla en el sheet cuando empieza un nuevo torneo
df_1 = pd.read_html(html)[0]

#Dejo el ejemplo de como lo actualizo en mi sheet yo, para que lo emulen. Tendrian que cambiar la ubicación de donde setean la sheet y su nombre.
gc = pygsheets.authorize(service_file={{creds}})
sheet = gc.open('Tabla Fútbol Argentino desde el 2000')
data = sheet[1]
data.set_dataframe(df_1, (939,2))

#Armo la tabla para actualizar el sheet.
df = data.get_as_df()
df.Equipo.replace(equivalenciaNombres, inplace=True)
tabla = df.groupby('Equipo',as_index=False).sum()
tabla_tot = tabla.drop(columns=['', 'Pos.']).drop(0).set_index('Equipo').drop('Equipo').sort_values(by='Pts.', ascending=False)
tabla_tot['Dif'] = tabla_tot['GF'] - tabla_tot['GC']
tabla_sheet = sheet[0]
tabla_sheet.set_dataframe(tabla_tot, (1,1), copy_index=True)
print('Actualizado el sheet')

#Armo visualización de la tabla y la exporto como png.
df_export = sheet[0].get_as_df()
df_export.index = range(1,df_export.shape[0]+1)
df_export = df_export.rename(columns={'':'Equipos'}).style.background_gradient()
hoy = date.today()
dfi.export(df_export, f'Tabla historica al {hoy}.png')
print(f'Guardado el archivo de {hoy}')
