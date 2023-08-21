#La sheet en la cual está la tabla es esta --> https://docs.google.com/spreadsheets/d/15CqzJhJH434Fqno_BSV_QVgsixlr2nM93nzDMOncY5k/edit?usp=sharing 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pygsheets
import dataframe_image as dfi
from datetime import date
from PIL import Image      
import tweepy
import imgkit


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

df = pd.read_html('https://www.promiedos.com.ar/primera')

df_1 = df[0]

gc = pygsheets.authorize(service_file='C:/Users/Federico Rábanos/Documents/lanus stats/creds.json')
sheet = gc.open('Tabla Fútbol Argentino desde el 2000')
data = sheet[1]
data.set_dataframe(df_1, (968,2))

df = data.get_as_df()
df.Equipo.replace(equivalenciaNombres, inplace=True)
tabla = df.groupby('Equipo',as_index=False).sum()
tabla_tot = tabla.drop(columns=['', 'Pos.']).drop(0).set_index('Equipo').drop('Equipo').sort_values(by='Pts.', ascending=False)
tabla_tot['Dif'] = tabla_tot['GF'] - tabla_tot['GC']
tabla_sheet = sheet[0]
tabla_sheet.set_dataframe(tabla_tot, (1,1), copy_index=True)
print('Actualizado el sheet')

df_export = sheet[0].get_as_df()
df_export.index = range(1,df_export.shape[0]+1)
df_export = df_export.rename(columns={'':'Equipos'}).style.background_gradient()
hoy = date.today()

dfi.export(df_export, f'C:/Users/Federico Rábanos/Documents/lanus stats/Python/Tablas/Tabla historica al {hoy}.png', table_conversion='matplotlib')
print(f'Guardado el archivo de {hoy}')

#api_key = "fWQW00ZBiJZ1sjL7mhCkKop40"
#api_secrets = "gyVY5Dmyn2e0o7lSTRvOeqKXkuqNIGWTu5LpuMUa1K4jXAjBY1"
#access_token = "1480711421465927688-3hpKYgsbT44DabSdc4D9kdkIPAXzB8"
#access_secret = "eJEmFzG0mIiyYF8d2Wu7apSwz2amRaHjQqEqLAdD0joFT"
#auth = tweepy.OAuthHandler(api_key,api_secrets)
#auth.set_access_token(access_token,access_secret)
#
#api = tweepy.API(auth, wait_on_rate_limit=True)
#print('iniciada la API instance')
#status = f'Tabla del Fútbol Argentino desde el 2000 al {hoy}'
#
#response = api.update_status_with_media(status=status, filename=f'C:/Users/Federico Rábanos/Documents/lanus stats/Python/Tablas/Tabla historica al {hoy}.png')