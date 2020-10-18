#!/usr/bin/env python
# coding: utf-8

# In[31]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class EvolucaoPopulacionalBM:
    """
    Classe para captura, limpeza e organizacao de dados existente na WORLDOMETERS relativo a evolucao populacao populacional dos paises de mundo
    Metodos:
    - parse
    - extrair_dados
    - converter_p_numeric
    - dados_paises
    """
    
    def __init__(self, urls):
        self.urls = urls
        

    # Extracao de Dados HTML
    def extrair_dados(self, url):
        cabecalho = []
        
        table = BeautifulSoup(requests.get(url).text, 'html.parser').find('div', {'class':'table-responsive'}).find('table')
        
        for entrada in table.find('tr').find_all('th'):
            cabecalho.append(entrada.text)

        dados = []
        for coluna in table.find('tbody').find_all('tr'):
            dados.append([valor.text for valor in coluna.find_all('td')])

        pais_df = pd.DataFrame(dados, columns=cabecalho)
        pais_df['Pais'] = url.replace('/', ' ').split()[-1]

        return pais_df



    # LIMPEZA de DADOS
    def converter_p_numerico(self, string):
        resultado = "".join([digito for digito in string if digito.isnumeric() or digito in '.-'])

        if resultado.replace('.','').replace('-','').isnumeric():
            return float(resultado)
        else:
            return np.nan




    # Uniao das Tabelas 
    def dados_paises(self):
        """ 
        urls: introduzida como uma lista (series de urls)
        """

       
        
        if type(self.urls) == str:
            try:
                return pd.concat([df, self.extrair_dados(self.urls)])
            except:
                print('Verifique a url (website link de Worldometers)')
            
        else:
            try:
                
                df = self.extrair_dados(self.urls[0])
                
                for url in self.urls[1:]:
                    print(f"{url[:-12].split('/')[-1]} \t {url}".expandtabs(20))
                    df = pd.concat([df, self.extrair_dados(url)])
                pais = df['Pais']
                df = df.iloc[:,:12]

                df[df.columns[2:]] = df.iloc[:, 2:].apply([self.converter_p_numerico])
                df['Pais'] = pais

                return df
            
            except:
                print('Verifique o conjunto de urls (Worldometers)')



    
    def para_numerico(self, obj):
        return int(''.join([car for car in obj if car.isnumeric()]))
    
    
    # Apartir da variavel inicial - cplp_paises (nomes de paises cplp) - criar nova variavel: evop_cplp (evol)    
    def evo_populacao(self):
        
        df = self.dados_paises()
        
        evo_populacional = pd.DataFrame()
        evo_populacional['Year'] = pd.to_datetime(df.Year.unique())
        lista_paises = [pais[::-1][11:][::-1]  for pais in df.Pais.unique()]

        for nome_pais in lista_paises:



            evo_populacional[nome_pais] = df[df.Pais.str.contains(nome_pais.lower().replace(' ', '-').replace('&', 'and'))]['Population']
            
        evo_populacional = evo_populacional.sort_values(['Year']).set_index(['Year'])
        
        for col in evo_populacional.columns:
            evo_populacional[col] = evo_populacional[col].apply(self.para_numerico)
            
        return evo_populacional

