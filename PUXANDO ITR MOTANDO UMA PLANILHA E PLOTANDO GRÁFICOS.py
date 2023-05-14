# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 19:00:37 2022

@author: lucas
"""

from zipfile import ZipFile
import wget
import pandas as pd
import os

# tipos de:    ENCONDING = ISO-8859-1 , utf-8, cp1252

#Selecionando o directorio de trabalho:
os.chdir('C:\\Users\\lucas\\OneDrive\\Área de Trabalho\\PROGRAMAS PYTHON\\TRABALHO ITR DE EMPRESAS') 

#Link dos arquivos .zip:
url_base  = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
url_base2 = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/'

#criando lista dos nomes dos arquivos:
arquivos_zip = []
for ano in range(2011,2023):
    arquivos_zip.append(f'itr_cia_aberta_{ano}.zip')


arquivos_zip2 = []
for ano in range(2011,2023):
    arquivos_zip2.append(f'dfp_cia_aberta_{ano}.zip')
    
#Download dos arquivos:
for arq in arquivos_zip:
    wget.download(url_base+arq)
    
for arq2 in arquivos_zip2:
    wget.download(url_base2+arq2)
    
#Decompactação dos arquivos:    
for arq in arquivos_zip:
    ZipFile(arq,'r').extractall('CVM_itr')
    
for arq2 in arquivos_zip2:
    ZipFile(arq2,'r').extractall('CVM_dfp')
    
#Criando listas para rodar na criação dos pre-fixos:
itr_nomes_ind = ['BPA_ind',
                 'BPP_ind',
                 'DRE_ind']

itr_nomes_con = ['BPA_con',
                 'BPP_con',
                 'DRE_con']

dfp_nomes_ind = ['BPA_ind',
                 'BPP_ind',
                 'DRE_ind']

dfp_nomes_con = ['BPA_con',
                 'BPP_con',
                 'DRE_con']

#Criando o DataFrame:
itr_df_ind = pd.DataFrame()   
for nome in itr_nomes_ind:
    for ano in range(2011,2023):
        itr_df_ind = pd.concat([itr_df_ind,pd.read_csv(f'C:\\Users\lucas\OneDrive\Área de Trabalho\PROGRAMAS PYTHON\TRABALHO ITR DE EMPRESAS\CVM_itr\itr_cia_aberta_{nome}_{ano}.csv',sep=';',decimal = ',',encoding = 'ISO-8859-1')]) 

itr_df_con = pd.DataFrame()         
for itr_nomes_con in itr_nomes_con:
    for ano in range(2011,2023):
        itr_df_con = pd.concat([itr_df_con,pd.read_csv(f'C:\\Users\lucas\OneDrive\Área de Trabalho\PROGRAMAS PYTHON\TRABALHO ITR DE EMPRESAS\CVM_itr\itr_cia_aberta_{itr_nomes_con}_{ano}.csv',sep=';',decimal = ',',encoding = 'ISO-8859-1')])
        
dfp_df_ind = pd.DataFrame()         
for dfp_nomes_ind in dfp_nomes_ind:
    for ano in range(2011,2023):
        dfp_df_ind = pd.concat([dfp_df_ind,pd.read_csv(f'C:\\Users\lucas\OneDrive\Área de Trabalho\PROGRAMAS PYTHON\TRABALHO ITR DE EMPRESAS\CVM_dfp\dfp_cia_aberta_{dfp_nomes_ind}_{ano}.csv',sep=';',decimal = ',',encoding = 'ISO-8859-1')])
        
dfp_df_con = pd.DataFrame()         
for dfp_nomes_con in dfp_nomes_con:
    for ano in range(2011,2023):
        dfp_df_con = pd.concat([dfp_df_con,pd.read_csv(f'C:\\Users\lucas\OneDrive\Área de Trabalho\PROGRAMAS PYTHON\TRABALHO ITR DE EMPRESAS\CVM_dfp\dfp_cia_aberta_{dfp_nomes_con}_{ano}.csv',sep=';',decimal = ',',encoding = 'ISO-8859-1')])


#Manipulação do DataFrame:
    
#Filtrando o Data Frame itr
itr_df_con = itr_df_con.loc[itr_df_con['ORDEM_EXERC'].isin(['ÚLTIMO'])]
itr_df_con = itr_df_con.loc[itr_df_con['CD_CONTA'].isin(['1','1.01','1.02','2.03','3.01','3.11','3.99.01.01'])]
#Filtrando o Data Frame dfp
dfp_df_con = dfp_df_con.loc[dfp_df_con['ORDEM_EXERC'].isin(['ÚLTIMO'])]
dfp_df_con = dfp_df_con.loc[dfp_df_con['CD_CONTA'].isin(['1','1.01','1.02','2.03','3.01','3.11','3.99.01.01'])]

#Juntando ambos os DataFrames consolidados após o filtro:
df_con = pd.concat([dfp_df_con,itr_df_con])

#Manipulando o DataFrame consolidado:
#Separamos o Data Frame em DRE, BPA e BPP
df_con_dre = df_con.loc[df_con['CD_CONTA'].isin(['3.01','3.11'])]
df_con_bpa = df_con.loc[df_con['CD_CONTA'].isin(['1','1.01'])]
df_con_bpp = df_con.loc[df_con['CD_CONTA'].isin(['2.03'])]  

#Coloando as coisas em ordem

df_con_dre = df_con_dre.sort_values(by= ['CD_CVM','CD_CONTA'])
df_con_bpa = df_con_bpa.sort_values(by= ['CD_CVM','CD_CONTA','DT_FIM_EXERC'])
df_con_bpp = df_con_bpp.sort_values(by= ['CD_CVM','CD_CONTA','DT_FIM_EXERC'])

#Resolvendo o DRE

df_con_dre = df_con_dre.drop_duplicates(['CD_CVM','DT_REFER','CD_CONTA'],keep = 'last')
df_con_dre = df_con_dre.sort_values(by= ['CD_CVM','CD_CONTA','DT_FIM_EXERC'])

df_final = pd.concat([df_con_dre,df_con_bpa,df_con_bpp])
df_final = df_final.sort_values(by = ['CD_CONTA','CD_CVM','DT_FIM_EXERC'])
df_final.to_excel('resultados.xlsx',sheet_name = 'resultados')
