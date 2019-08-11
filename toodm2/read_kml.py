
from fastkml import kml
import pandas as pd

filename='OUTORGAS_SUPERFICIAIS_AL_JAN2001_JUL2018.kml'
with open(filename, 'rt') as f:
    doc = f.read().encode('utf-8')
    lista = str(doc).split('\\n')


#Para o Dicionario
dicio = {}
colunas = ['FID', 'ITEM', 'PROCESSO', 'PORTARIA', 'ANO PORTAR',
'DATA EXTRA', 'VALIDADE', 'VENCIMENTO', 'SITUACAO', 'PLEITO',
'FINALIDADE', 'TIPO MANAN', 'BACIA/AQUI', 'MUNICIPIO', 'CPF/CNPJ',
'USUARIO', 'QOUT_m?/h', 'QOUT_m3/s', 'NIVEL ES_m', 'NIVEL DI_m',
'DURACAO_h', 'FUSO', 'UTM E_m', 'UTM N_m', 'LAT GRAU', 'LAT MINUTO',
'LAT SEGUND', 'LONG GRAU', 'LONG MINUT','LONG SEGUN', 'LATITUDE',
'LONGITUDE', 'NOTA','OBS_PROCES', 'OBS_PORTAR', 'CNARH']
for col in colunas:
    dicio[col]=[]

#Leitura e organização
matriz = []
linha = []
for item in range(len(lista)):

    if 'FID' in lista[item]:
        linha.append(lista[item+2])

    elif 'ITEM' in lista[item]:
        linha.append(lista[item+2])

    elif 'PROCESSO' in lista[item]:
        linha.append(lista[item+2])

    elif 'PORTARIA' in lista[item]:
        linha.append(lista[item+2])

    elif 'ANO PORTAR' in lista[item]:
        linha.append(lista[item+2])

    elif 'DATA EXTRA' in lista[item]:
        linha.append(lista[item+2])

    elif 'VALIDADE' in lista[item]:
        linha.append(lista[item+2])

    elif 'VENCIMENTO' in lista[item]:
        linha.append(lista[item+2])

    elif 'SITUACAO' in lista[item]:
        linha.append(lista[item+2])

    elif 'PLEITO' in lista[item]:
        linha.append(lista[item+2])

    elif 'FINALIDADE' in lista[item]:
        linha.append(lista[item+2])

    elif 'TIPO MANAN' in lista[item]:
        linha.append(lista[item+2])

    elif 'BACIA/AQUI' in lista[item]:
        linha.append(lista[item+2])

    elif 'MUNICIPIO' in lista[item]:
        linha.append(lista[item+2])

    elif 'CPF/CNPJ' in lista[item]:
        linha.append(lista[item+2])

    elif 'USUARIO' in lista[item]:
        linha.append(lista[item+2])

    elif 'QOUT_m?/h' in lista[item]:
        linha.append(lista[item+2])

    elif 'QOUT_m3/s' in lista[item]:
        linha.append(lista[item+2])

    elif 'NIVEL ES_m' in lista[item]:
        linha.append(lista[item+2])

    elif 'NIVEL DI_m' in lista[item]:
        linha.append(lista[item+2])

    elif 'DURACAO_h' in lista[item]:
        linha.append(lista[item+2])

    elif 'FUSO' in lista[item]:
        linha.append(lista[item+2])

    elif 'UTM E_m' in lista[item]:
        linha.append(lista[item+2])

    elif 'UTM N_m' in lista[item]:
        linha.append(lista[item+2])

    elif 'LAT GRAU' in lista[item]:
        linha.append(lista[item+2])

    elif 'LAT MINUTO' in lista[item]:
        linha.append(lista[item+2])

    elif 'LAT SEGUND' in lista[item]:
        linha.append(lista[item+2])

    elif 'LONG GRAU' in lista[item]:
        linha.append(lista[item+2])

    elif 'LONG MINUT' in lista[item]:
        linha.append(lista[item+2])

    elif 'LONG SEGUN' in lista[item]:
        linha.append(lista[item+2])

    elif 'LATITUDE' in lista[item]:
        linha.append(lista[item+2])

    elif 'LONGITUDE' in lista[item]:
        linha.append(lista[item+2])

    elif 'NOTA' in lista[item]:
        linha.append(lista[item+2])

    elif 'OBS_PROCES' in lista[item]:
        linha.append(lista[item+2])

    elif 'OBS_PORTAR' in lista[item]:
        linha.append(lista[item+2])

    elif 'CNARH' in lista[item]:
        linha.append(lista[item+2])

        #tratamento
        for i in linha:
            if i == '</tr>':
                linha.remove('</tr>')
        #Retirar excessos
        for i in range(len(linha)):
            linha[i] = linha[i].replace('<td>', '')
            linha[i] = linha[i].replace('</td>', '')

        #Inserindo no Dicionario
        for i in range(len(linha)):
            dicio[colunas[i]].append(linha[i])


        matriz.append(linha)
        linha = []
#pd.set_option('display.max_columns', 500)
df = pd.DataFrame(dicio)

#with pd.option_context('display.max_rows', None):
    #print(df)
