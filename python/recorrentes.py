import pandas as pd
import numpy as np

def filtraperiodo(df, campo, valor):
  dfr = df.copy()
  isperiodo = dfr[campo] == valor
  dfr = dfr[isperiodo]
  return dfr

def calc(df,campo,periodo,delta,nome,medias2,medias10,calcularmedia):
  idx = periodo + delta
  if calcularmedia:
    calculado = df[campo].mean()
  else:
    calculado = df[campo].std()
  if campo == 'PM2.5':
    for i in range(len(medias2[idx][0])):
      if medias2[idx][0][i] == nome:
        medias2[idx][1][i] = calculado
        break
  else:
    for i in range(len(medias10[idx][0])):
      if medias10[idx][0][i] == nome:
        medias10[idx][1][i] = calculado
        break

def processaumcampo(campofiltragem,totalvalores,delta,calcularmedia):
  #estacoes = ['Aotizhongxin','Wanshouxigong']
  estacoes = ['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']
  estacg = estacoes.copy()
  estacg.append('Geral')
  # uma cópia para cada período mais os totais gerais
  medias10=[]
  medias2=[]
  # um vetor por período mais os totais
  for i in range(totalvalores+1):
    # uma coluna de nomes mais duas para as médias e desvios correspondentes
    medias10.append([estacg.copy(), []])
    medias2.append([estacg.copy(), []])
    for j in range(len(estacg)):
      medias10[i][1].append(0)
      medias2[i][1].append(0)

  # escolhe campos que não serão fitrados para facilitar  
  dfx = pd.read_csv('preprocessado.csv', parse_dates=[], index_col=['Dia normalizado','Latitude','Longitude'])

  #cálculos de médias e desvios
  nome='Geral'
  df = dfx.copy()
  if delta==0:
    calc(df,'PM2.5',totalvalores+1,-1,nome,medias2,medias10,calcularmedia)
    calc(df,'PM10', totalvalores+1,-1,nome,medias2,medias10,calcularmedia)
  else:
    calc(df,'PM2.5',totalvalores+1,delta,nome,medias2,medias10,calcularmedia)
    calc(df,'PM10', totalvalores+1,delta,nome,medias2,medias10,calcularmedia)
  for i in range(totalvalores):
    dfp = filtraperiodo(df,campofiltragem,i-delta)
    calc(dfp,'PM2.5',i-delta,delta,nome,medias2,medias10,calcularmedia)
    calc(dfp,'PM10',i-delta,delta,nome,medias2,medias10,calcularmedia)

  # loop de montagem de estatísticas por estação
  for nome in estacoes:
    is_estacaoespecifica = dfx['station'] == nome
    df = dfx[is_estacaoespecifica]
    if delta==0:
      calc(df,'PM2.5',totalvalores+1,-1,nome,medias2,medias10,calcularmedia)
      calc(df,'PM10', totalvalores+1,-1,nome,medias2,medias10,calcularmedia)
    else:
      calc(df,'PM2.5',totalvalores+1,delta,nome,medias2,medias10,calcularmedia)
      calc(df,'PM10', totalvalores+1,delta,nome,medias2,medias10,calcularmedia)
    for i in range(totalvalores):
      dfp = filtraperiodo(df,campofiltragem,i-delta)
      calc(dfp,'PM2.5',i-delta,delta,nome,medias2,medias10,calcularmedia)
      calc(dfp,'PM10',i-delta,delta,nome,medias2,medias10,calcularmedia)

  for i in range(totalvalores+1):
    print(campofiltragem+str(i-delta))
    if calcularmedia:
      with open(campofiltragem+str(i-delta)+'_m25.csv', 'w') as fp:
        np.savetxt(fp,medias2[i],'%s',',')
      with open(campofiltragem+str(i-delta)+'_m10.csv', 'w') as fp:
        np.savetxt(fp,medias10[i],'%s',',')
    else:
      with open(campofiltragem+str(i-delta)+'_d25.csv', 'w') as fp:
        np.savetxt(fp,medias2[i],'%s',',')
      with open(campofiltragem+str(i-delta)+'_d10.csv', 'w') as fp:
        np.savetxt(fp,medias10[i],'%s',',')
      
# rotina principal

# médias
processaumcampo('month',12,-1,True)
processaumcampo('day',31,-1,True)
processaumcampo('dia da semana',7,-1,True)
processaumcampo('hour',24,0,True)

# desvios-padrões
#processaumcampo('month',12,-1,False)
#processaumcampo('day',31,-1,False)
#processaumcampo('dia da semana',7,-1,False)
#processaumcampo('hour',24,0,False)
