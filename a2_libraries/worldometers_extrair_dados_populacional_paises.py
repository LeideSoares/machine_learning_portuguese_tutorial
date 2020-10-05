import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# Conexao com servidor de Barometro Mundial
def parser( url):
    table = BeautifulSoup(requests.get(url).text, 'html.parser').find('div', {'class':'table-responsive'}).find('table')
    return table



# Extracao de Dados HTML
def extrair_dados(url):

    table = parser(url)

    cabecalho = []


    for entrada in table.find('tr').find_all('th'):
        cabecalho.append(entrada.text)
   

    dados = []
    for coluna in table.find('tbody').find_all('tr'):
        dados.append([valor.text for valor in coluna.find_all('td')])
    
    pais_df = pd.DataFrame(dados, columns=cabecalho)
    
    pais_df['Pais'] = url.replace('/', ' ').split()[-1]
    
    return pais_df



# LIMPEZA de DADOS

def converter_p_numerico(string):
    resulado = "".join([digito for digito in string if digito.isnumeric() or digito in '.-'])
    
    if resulado.replace('.','').replace('-','').isnumeric():
        return float(resulado)
    else:
        return np.nan
    
    
    

# Uniao das Tabelas 
def dados_paises(urls):
    """ 
    url: introduzida como uma lista (series de urls)
    """
    
    columns = [ 
                'Pais', 'Year', 'Population', 'Yearly %  Change', 'Yearly Change', 'Migrants (net)', 
                'Median Age', 'Fertility Rate', 'Density (P/Km²)', 'Urban Pop %', 'Urban Population',
                "Country's Share of World Pop", 'World Population'
            ]
    
    df =  pd.DataFrame(columns=columns)
    
    for url in urls:
        print(url)
        df = pd.concat([df, extrair_dados(url)])
    
    df = df.iloc[:,:12]
    
    df[df.columns[2:]] = df.iloc[:, 2:].apply([converter_p_numerico])
    return df


