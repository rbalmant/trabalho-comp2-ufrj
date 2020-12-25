# trabalho-comp2-ufrj

## Trabalho final da disciplina Computação II da UFRJ.
Se trata de um programa que dispôe em uma projeção do mapa terrestre os tweets mais relevantes (trending topics), de acordo com a localização geográfica (quando disponível). Um complicação foi tentar fazer com a aplicação rodasse em tempo real, pois a biblioteca tweepy infelizmente não expõe a thread que utiliza.

## Ferramentas utilizadas: 
    - Tkinter
    - matplotlib
    - Basemap
    - tweepy

Para a aplicação rodar é preciso obter as credenciais de acesso à API do twitter e colocá-las no arquivo twitter.ini
É possível mudar a projeção utilizada e algumas configurações de cor no arquivo map.ini também.
