import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tki

def filtraano(df, inicial, final):
  dfr = df.copy()
  isinf = dfr['No'] >= inicial
  issup = dfr['No'] <= final
  dfr = dfr[isinf]
  dfr = dfr[issup]
  return dfr

def calc(df,campo,ano):
  idx = int(ano) - 2013
  media = df[campo].mean()
  dev = df[campo].std()
  if campo == 'PM2.5':
    for i in range(len(medias2[idx][0])):
      if medias2[idx][0][i] == nome:
        medias2[idx][1][i] = media
        medias2[idx][2][i] = dev
        break
  else:
    for i in range(len(medias10[idx][0])):
      if medias10[idx][0][i] == nome:
        medias10[idx][1][i] = media
        medias10[idx][2][i] = dev
        break
  #print('Média '+nome+' '+campo+' '+ano+' '+str(media))
  #print('Desvio '+nome+' '+campo+' '+ano+' '+str(dev))
  
def plotaserie4anos(df2013,df2014,df2015,df2016,campo):
  plt.figure(figsize=(16,5), dpi=100)
  s=df2013[campo]
  s.plot(color='tab:red',label='2013')
  s=df2014[campo]
  s.plot(color='tab:orange',label='2014')
  s=df2015[campo]
  s.plot(color='tab:blue',label='2015')
  s=df2016[campo]
  s.plot(color='tab:green',label='2016')
  plt.gca().set(title=nome + " - 2013 a 2016", xlabel='Dia',ylabel=campo)
  plt.legend();
  plt.show()
  calc(df2013,campo,'2013')
  calc(df2014,campo,'2014')
  calc(df2015,campo,'2015')
  calc(df2016,campo,'2016')

#estacoes = ['Aotizhongxin','Wanshouxigong']
estacoes = ['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']
estacg = estacoes.copy()
estacg.append('Geral')
# uma cópia para cada ano mais os totais gerais
medias10=[]
medias2=[]
# um vetor por ano mais os totais
for i in range(5):
  # uma coluna de nomes mais duas para as médias e desvios correspondentes
  medias10.append([estacg.copy(), [], []])
  medias2.append([estacg.copy(), [], []])
  for j in range(len(estacg)):
    medias10[i][1].append(0)
    medias2[i][1].append(0)
    medias10[i][2].append(0)
    medias2[i][2].append(0)

# escolhe campos que não serão fitrados para facilitar  
dfx = pd.read_csv('preprocessado.csv', parse_dates=[], index_col=['Dia normalizado','Latitude','Longitude'])

#cálculos de médias e desvios
nome='Geral'
df = dfx.copy()
calc(df,'PM2.5','2017')
calc(df,'PM10','2017')
df2013 = filtraano(df,1,8760)
df2014 = filtraano(df,8761,17520)
df2014['No'] = df2014['No']-8760
df2015 = filtraano(df,17521,26304)
df2015['No'] = df2015['No']-17520
df2016 = filtraano(df,26305,35064)
df2016['No'] = df2016['No']-26304
df2013=df2013.set_index('No')
df2014=df2014.set_index('No')
df2015=df2015.set_index('No')
df2016=df2016.set_index('No')
calc(df2013,'PM2.5','2013')
calc(df2014,'PM2.5','2014')
calc(df2015,'PM2.5','2015')
calc(df2016,'PM2.5','2016')
calc(df2013,'PM10','2013')
calc(df2014,'PM10','2014')
calc(df2015,'PM10','2015')
calc(df2016,'PM10','2016')

# loop de montagem de gráficos e estatísticas por estação
for nome in estacoes:
  is_estacaoespecifica = dfx['station'] == nome
  df = dfx[is_estacaoespecifica]
  calc(df,'PM2.5','2017')
  calc(df,'PM10','2017')
  df2013 = filtraano(df,1,8760)
  df2014 = filtraano(df,8761,17520)
  df2014['No'] = df2014['No']-8760
  df2015 = filtraano(df,17521,26304)
  df2015['No'] = df2015['No']-17520
  df2016 = filtraano(df,26305,35064)
  df2016['No'] = df2016['No']-26304
  df2013=df2013.set_index('No')
  df2014=df2014.set_index('No')
  df2015=df2015.set_index('No')
  df2016=df2016.set_index('No')
  plotaserie4anos(df2013,df2014,df2015,df2016,'PM2.5')
  plotaserie4anos(df2013,df2014,df2015,df2016,'PM10')

for i in range(5):
  print(2013+i)
  print(medias2[i])
  print(medias10[i])
