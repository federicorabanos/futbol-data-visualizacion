import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen
from mplsoccer import Pitch, add_image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def getImage(path, zoom=1):
    return OffsetImage(path, zoom=zoom)

class TresSeisCincoScores:

    def parsear_dataframe(self, objeto):
        df = pd.DataFrame(objeto['rows'])
        df_1 = df['entity'].apply(pd.Series)
        df_2 = df['stats'].apply(pd.Series)[0].apply(pd.Series)
        df_concat = pd.concat([df_1, df_2], axis=1)[['id', 'name', 'positionName', 'value']]
        df_concat['estadistica'] = objeto['name']
        return df_concat

    def scrapear_estadisticas_liga(self, league_id):
        response = requests.get(f'https://webws.365scores.com/web/stats/?appTypeId=5&langId=29&timezoneName=America/Buenos_Aires&userCountryId=382&competitions={league_id}&competitors=&withSeasons=true')
        estadisticas = response.json()
        estadisticas_generales = estadisticas['stats']
        df_total = pd.DataFrame()
        for i in range(len(estadisticas_generales)):
            objeto = estadisticas_generales[i]
            stats_df = self.parsear_dataframe(objeto)
            df_total = pd.concat([df_total, stats_df])
        return df_total

    def ids_ligas():
        id_ligas = {
            'Brasileirao': 113,
            'Champions League': 572,
            'Liga BetPlay': 620,
            'Copa de la Liga': 7214
        }
        return id_ligas
    
    def sacar_data_partido(self, game_id, matchup_id):
        response = requests.get(f'https://webws.365scores.com/web/game/?appTypeId=5&langId=29&timezoneName=America/Buenos_Aires&userCountryId=382&gameId={game_id}&matchupId={matchup_id}&topBookmaker=14')
        data_partido = response.json()['game']
        return data_partido
    
    def sacar_tiros(self, data_partido):
        json_tiros = data_partido['chartEvents']['events']
        df = pd.DataFrame(json_tiros)
        return df
    
    def sacar_informacion_jugadores(self, data_partido):
        json_equipos = data_partido['members']
        df_equipos = pd.DataFrame(json_equipos)
        return df_equipos
    
    def nombres_equipos(self, data_partido):
        valores = ['home', 'away']
        nombres = []
        for valor in valores:
            nombre = data_partido[f'{valor}Competitor']['name']
            nombres.append(nombre)
        local, visitante = nombres[0], nombres[1]
        return local, visitante
    
    def sacar_estadisticas_partido_generales(self, game_id, matchup_id):
        data_partido = self.sacar_data_partido(game_id, matchup_id)
        valores = ['home', 'away']
        df_total = pd.DataFrame()
        for valor in valores:
            df = pd.DataFrame(data_partido[f'{valor}Competitor']['statistics'])[['name', 'categoryName', 'value']]
            df['equipo'] = data_partido[f'{valor}Competitor']['name']
            df_total = pd.concat([df_total, df]).reset_index(drop=True)
        return df_total

    def sacar_mapa_calor(self, jugador, game_id, matchup_id):
        data_partido = self.sacar_data_partido(game_id, matchup_id)
        jugadores = data_partido['homeCompetitor']['lineups']['members']
        df_jugadores = pd.DataFrame(jugadores)
        jugadores_total = pd.DataFrame(data_partido['members'])
        df_jugadores = df_jugadores.merge(jugadores_total, on='id', how='left')
        heatmap = Image.open(urlopen(df_jugadores[df_jugadores['name'] == jugador].heatMap.iloc[0]))
        return heatmap
