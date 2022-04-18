#La sheet en la cual está la tabla es esta --> https://docs.google.com/spreadsheets/d/15CqzJhJH434Fqno_BSV_QVgsixlr2nM93nzDMOncY5k/edit?usp=sharing 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pygsheets

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
'Union': 'Unión'}

#Armo driver con selenium para sacar tablas de Promiedos.
options = Options()
path = "C:/Users/Federico Rábanos/.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver.exe"
driver = webdriver.Chrome(path, options=options)
driver.get('https://www.promiedos.com.ar/copadeliga')
html = driver.page_source
driver.close()

df_1 = pd.read_html(html)[0]
df_2 = pd.read_html(html)[1]

gc = pygsheets.authorize(service_file='C:/Users/Federico Rábanos/Documents/lanus stats/creds.json')
sheet = gc.open('Tabla Historica')
data = sheet[0]
data.set_dataframe(df_1, (909,2))
data.set_dataframe(df_2, (909+df_1.shape[0]+1,2))

df = data.get_as_df()
df.Equipo.replace(equivalenciaNombres, inplace=True)
tabla = df.groupby('Equipo',as_index=False).sum()
tabla_tot = tabla.drop(columns=['', 'Pos.']).drop(0).set_index('Equipo').drop('Equipo').sort_values(by='Pts.', ascending=False)
tabla_tot['Dif'] = tabla_tot['GF'] - tabla_tot['GC']
tabla_sheet = sheet[1]
tabla_sheet.set_dataframe(tabla_tot, (1,1), copy_index=True)
print('Finalizado con exito')