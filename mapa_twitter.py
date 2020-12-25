#!/usr/bin/env python
# -*- encoding:utf-8 -*-

""" Captura tweets mundiais dos trending topics, desenha o mapa mundi e então plota pontos a partir das coordenadas de cada tweet (quando disponíveis) """


# Mapa
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
# Garante o uso do Tk
matplotlib.use('TKAgg')

# Mensagem de erro
from tkMessageBox import showerror

# sys.exit() e datetime.datetime.now()
import sys
import datetime
# Twitter
import tweepy

# Tamanho da bolinha será aleatório
from random import randint

CONFIG_MAP_PATH_TO_FILE = "map.ini"
CONFIG_TWITTER_PATH_TO_FILE = "twitter.ini"
MAX_RADIUS = 15

class Config:
	""" Desserializa um arquivo de configuração genérico do tipo "NOME_CONFIG=VALOR_CONFIG;NOME_CONFIG=VALOR_CONFIG" """
	def __init__(self, config_file):
		self.__config = self.__read_config_file(config_file)

	def __read_config_file(self, config_file):
		file_content = ''
		config = {}
		try:
			with open(config_file, "r") as file:
				file_content = file.read().split(";")
				for line in file_content:
					config_line = line.split("=")
					config[config_line[0]] = config_line[-1]
			return config
		except IOError:
			showerror("I/O error", "Couldn't open file {}".format(config_file))
			sys.exit(1)

	def get_config(self, config_key):
		try:
			return self.__config[config_key]
		except KeyError:
			showerror("Config key", "Config key {} not found".format(config_key))
			sys.exit(1)

class Map:
	# Gerencia o desenho do mapa e pontos na tela
	def __init__(self, master, config_file="map.ini"):
		self.__config = Config(config_file)
		self.map = Basemap(projection=self.__config.get_config("PROJECTION"), resolution=self.__config.get_config("RESOLUTION"), lon_0=0)	
		self.map.drawcoastlines()
		self.map.drawmapboundary(fill_color=self.__config.get_config("OCEAN_COLOR"))
		self.map.fillcontinents(color=self.__config.get_config("CONTINENT_COLOR"), lake_color=self.__config.get_config("LAKE_COLOR"))

	def plot_point(self, lat, lon, radius):
		# Desenha o ponto no mapa
		x, y = self.map(lon, lat)
		self.map.plot(x, y, 'bo', markersize=radius, alpha=0.6)

class AuthHandler:
	""" Responsável pelo processo de autenticação do Twitter """
	def __init__(self, config_file="twitter.ini"):
		self.__config = Config(config_file)
		self.__auth = tweepy.OAuthHandler(self.__config.get_config("CONSUMER_KEY"), self.__config.get_config("CONSUMER_SECRET"))
		self.__auth.set_access_token(self.__config.get_config("ACCESS_TOKEN"), self.__config.get_config("ACCESS_TOKEN_SECRET"))
		self.api = tweepy.API(self.__auth)

class TrendsStreamListener(tweepy.StreamListener):
	def __init__(self, auth_handler):
		self.map = Map(CONFIG_MAP_PATH_TO_FILE)
		self.api = auth_handler.api
		self.stream = tweepy.Stream(auth=self.api.auth, listener=self)
		self.get_new_trends()
	
	def get_new_trends(self):
        	# Pega os Trending Topics mundiais (Yahoo Where On Earth ID (WOEID) = 1)
		trends_json = self.api.trends_place(id=1)
		trends_data = trends_json[0]
		trends = trends_data['trends']
        	# Pega os nomes crus dos Trending Topics
		trends_name = [trend['name'] for trend in trends]
        	# Começa a escutar por essas palavras
		self.stream.filter(track=trends_name, async=True)

	def on_status(self, tweet):
		if (tweet.coordinates != None):
			print ("[" + str(datetime.datetime.now()) + "] Novo tweet localizado. Coordenadas: " + str(tweet.coordinates['coordinates']))
			# Manda desenhar o ponto do tweet no mapa
			self.map.plot_point(tweet.coordinates['coordinates'][1], tweet.coordinates['coordinates'][0], randint(5, MAX_RADIUS))
			
	def on_error(self, status):
		# Se houver algum erro da API do twitter, saberemos aqui
		print ("[" + str(datetime.datetime.now()) + "] " + str(status))


MY_AUTH_HANDLER = AuthHandler()
TRENDS_STREAM_LISTENER = TrendsStreamListener(MY_AUTH_HANDLER)

# Tweepy está rodando em um thread (e portanto chamará Map.plot_point() por si só), podemos então redesenhar o mapa inteiro a cada 0.05s, e esse será o único comando de desenho do nosso programa. 
while(True):
	plt.pause(0.05)

# Nada roda aqui
# print "hello"

