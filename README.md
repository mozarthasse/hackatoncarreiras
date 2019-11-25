# hackatoncarreiras
Trabalho para o hackaton de carreiras

## 1. Questões de pesquisa e justificativas:

### Qual a amplitude e variação nos valores dos campos?
- justificativa: necessário para verificar a integridade dos dados e para tirar conclusões mais evidentes ou que possam direcionar os passos seguintes na pesquisa.

### Existem correlações relevantes entre os campos?
- justificativa: descobrir e/ou eliminar as conclusões mais triviais antes de tentar mecanismos mais elaborados de análise.

### Existem tendências ou padrões recorrentes nos dados?
- justificativa: buscar por padrões cíclicos que expliquem a maior parte da variação nos valores e permita identificar tendências e ter alguma previsibilidade.

As hipóteses mais óbvias a analisar consistem em identificar a presença ou ausência de padrões:

- anuais
- mensais
- semanais
- diários


### Os dados seguem alguma tendência ao longo do período estudado?
- verificar se há alguma indicação de que os índices estão subindo ou descendo a longo prazo.

### Considerando que são dados coletados em regiões próximas, existe correlação entre os valores obtidos nas diversas estações?
- verificar se há efeito mensurável na difusão dos poluentes em função da proximidade entre as estações.


## 2. Ferramentas usadas

- Linux Ubuntu: software livre base para uso de todos os outros, incluindo o bash para o processamento trivial de arquivos.
Site: https://ubuntu.com/download/desktop , versão 18.04.3 LTS

- Libreoffice Calc: colocar fórmulas numa planilha ajuda no processamento mais trivial como a criação de campos complementares em formato adequado para análise. Site: https://pt-br.libreoffice.org/ , versão 6.0.7.3

- Weka: a disponibilidade de algoritmos de inteligência artifical, mineração de dados e ferramentas de tratamento básicos dos dados são convenientes para responder perguntas que porventura surjam durante a análise. Site: https://www.cs.waikato.ac.nz/ml/weka/ , versão 3.8.1

- Python: linguagem prática e rápida para transformar em imagens os dados e ajudar no direcionamento da análise. Instalada a partir do próprio Ubuntu, pacote ```python3-pip``` e dependências. Usando o utilitário ```pip3```, instalar também  
os pacotes ```wheel``` e ```pandas```.
Site: https://www.python.org/ , VERSÃO EXIGIDA 3.6.8 (nem maior nem menor)

É possível usar o Visual Studio Code (com os devidos plugins) para visualizar e depurar o código. Também é possível executar diretamente da linha de comando qualquer dos pogramas criados, bastando para isso que os arquivos de dados de entrada tenham sido gerados e o arquivo ```preprocessado.csv``` esteja na mesma pasta.


## 3. Tratamento dos dados e métodos usados

### 3.1. Junção dos dados em um único arquivo CSV com todos os campos tratados

Resumo macro:
```
  PRSA_Data_20130301-20170228 + junta.sh (bash)=> junto.csv
  junto.csv (abrir)=> preprocessamento.ods
  preprocessamento.ods (salvar como)=> preprocessado.csv + cabecalho.arff
```

Decidiu-se juntar os dados de todas as estações em um único arquivo para facilitar o processamento via planilha. Usou-se para isso o arquivo ```junta.sh```, que transforma todos os arquivos em um único chamado ```junto.csv```

Depois, abre-se o arquivo ```junto.csv``` dentro do LibreOffice, na planilha ```junto``` do arquivo ```preprocessamento.ods``` tomando o cuidado de configurar todos os campos numéricos para o formato "Inglês(EUA)" (ponto decimal ao invés de vírgula).

Os campos criados na planilha foram:
- dia da semana: valor de 1 a 7 deduzido dos campos ```year```, ```month```, ```day```. Coluna ```E```, fórmula ```=DIA.DA.SEMANA(DATA(B2;C2;D2))```
- dia normalizado: campo para tratar a data como sendo um valor numérico contínuo.Considera como fração o número de horas desde o começo do ano até o dia e hora da medição. Pode ser mais conveniente para identificar correlações ou fazer previsões sazonais.  Coluna ```G```, fórmula ```=B2+((DATA(B2;C2;D2)-DATA(B2;1;1))+F2/24)/366```
- ângulo do vento: transforma o campo texto em um valor numérico para facilitar a eventual busca de correlações entre o grau de poluição da estação pesquisada e a vizinhança caso o vento seja identificado como fator relevante. Coluna ```S```, fórmula ```=PROCV(R2;Ângulos.$A$1:$B$17;2;0)```
- latitude e longitude: posição APROXIMADA de cada estação para que se possa oportunamente medir distâncias entre elas e analisar mais a fundo a contribuição do vento para carregar a poluição entre estações próximas. Não foi encontrada a localização EXATA, porém é possível deduzir as coordenadas GPS fazendo uma regra-de-três entre os gráficos exibidos em artigos que já analisaram esta base de dados e as coordenadas GPS de dois pontos no mapa seja razoavelmente conhecida. Mesmo reconhecidamente inadequada para tirar conclusões impecáveis sobre essas correlações, esta aproximação já ajuda BASTANTE a representar visualmente o comportamento dos dados. os detalhes destes cálculos estão na planilha ```coordenadas.ods```. Colunas ```V``` e ```W```, com as fórmulas ```=PROCV(U2;Coordenadas.$A$1:$C$12;2;0)``` e ```=PROCV(U2;Coordenadas.$A$1:$C$12;3;0)```, respectivamente.

Todos estes campos e suas fórmulas estão no arquivo ```preprocessamento.ods```. Ele deve ser transformado novamente em csv
selecionando-se a primeira planilha do arquivo e mandando salvá-la como ```preprocessado.csv```. NÃO colocar aspas em todas as células de texto e mandar salvar o conteúdo das células como mostrado para preservar o ponto decimal e número de casas decimais.

### 3.2. Preparação para uso do Weka

Resumo macro:
  ```junta2.sh + cabecalho.arff + preprocessado.csv (bash)=> entrada*.arff```

O formato do Weka é praticamente igual ao csv, sendo necessário apenas acrescentar um cabeçalho (arquivo ```cabecalho.arff``` gerado a partir do ```preprocessamento.ods```). Um cuidado foi tomado para tornar os dados mais convenientes para o Weka: todos os campos não preenchidos (valores ```NA```) foram trocados para ```?```, que é o padrão do Weka para este caso.

A conversão de csv para arff foi feita através da execução do arquivo ```junta2.sh```. Neste arquivo foram feitas versões separadas das estações (```entrada1.arff``` a ```entrada12.arff```) para que se possa oportunamente usar os pacotes de tratamento (http://weka.sourceforge.net/doc.packages/timeSeriesFilters) e previsão de séries temporais (http://wiki.pentaho.com/display/DATAMINING/Time+Series+Analysis+and+Forecasting+with+Weka).

### 3.3. Montagem e totalização das médias/desvios via Python para as planilhas de totalização

Resumo macro:
```
  preprocessado.csv (bash mv)=> python\preprocessado.csv
  python\preprocessado.csv + visual.py (python3)=> gráficos por estação + saída de texto (colagem manual)=> anuais.ods
  python\preprocessado.csv + recorrentes.py (python3)=> month*_m*.csv + day*_m*.csv + 'dia da semana*_m*.csv' + hour*_m*.csv
```

Os gráficos das tendências anuais foram gerados diretamente pelo Python devido ao volume de dados, grande demais para que uma planilha consiga manipular com desempenho razoável. Aproveitou-se o mesmo código para calcular os desvios-padrões e médias anuais, que foram transcritos para a planilha ```anuais.ods```. Preferiu-se dividir os dados por estação para conferir se existem divergências relevantes na variação de dados entre os indicadores ou entre as estações.


Gráficos foram montados para cada indicador e métrica e foram anexados na mesma planilha onde fica a tabela de dados correspondente.  A média geral foi destacada nos gráficos para facilitar a identificação das estações com medições significativamente acima ou abaixo da média geral para o mesmo dia, mês ou hora.


A montagem das tabelas foi obtida a partir da saída do programa ```recorrentes.py```, que gera um arquivo por indicador, poluente e valor. Um arquivo adicional (com o valor máximo possível+1) foi gerado para cada métrica para registrar as médias de todos os dados e anos para o valor respectivo. Por exemplo: os arquivos day32_m25.csv e day32_m10.csv corresponde aos totais dos poluentes PM2.5 e PM10 por estação, respectivamente. Estes arquivos, mesmo que redundantes, facilitam a montagem da tabela presente nas planilhas e tornam mais fácil a comparação de valores e identificação de quais estações e valores ficam acima ou abaixo da média.  


### 3.4. Montagem das planilhas de totalização

Resumo macro:
```
  montastats.sh + month*_m*.csv + day*_m*.csv + 'dia da semana*_m*.csv' + hour*_m*.csv (bash)=> month??.csv + day??.csv + semana??.csv + hour??.csv
  month??.csv + day??.csv + semana??.csv + hour??.csv (colagem anual)=> mensais.ods + dários.ods + semanais.ods + porhora.ods
```
  
Todos os arquivos gerados via python foram agrupados na ordem adequada para formar as tabelas colocadas nas planilhas correspondentes. Esta montagem em etapas não é muito eficiente mas é prática e rápida considerando o volume de dados e o tempo de processamento. Se os dados fossem outros ou os valores tivessem maior variedade, seriam necessárias outras automações, porém dado o tempo disponível e o objetivo do trabalho isso não foi considerado prioritário. Diversos pontos do processo poderiam passar por automações e simplificações caso estes dados tivessem maior volume ou sofressem atualização constante.


## 4. Resultados coletados

Os resultados coletados foram organizados conforme sua relevância para responder às perguntas planejadas.

### Qual a amplitude e variação nos valores dos campos?

Ao abrir o Weka, usar o explorer, abrir o arquivo entrada.arff clicar no campo correspondente, é possível obter os histogramas de todos os campos, assim como mínimos, máximos, médias e desvios-padrões respectivos. Os resultados foram colocados na planilha ```Weka/estatisticas.ods```. Alguns campos (SO2, NO2 e O3) têm uma variação enorme nos valores e aparentemente pouca utilidade preditiva.


Já os campos PM2.5, PM10, CO e a intensidade do vento possuem histogramas similares e tiveram sua correlação confirmada pelo Weka através de outro processo.

### Existem correlações relevantes entre os campos?

A capacidade preditiva dos campos foi medida com o uso do algoritmo "Correlation-based Feature Subset Selection", identificado no Weka como ```weka.attributeSelection.CfsSubsetEval```. Foi usado o mecanismo 10-fold cross-validation para minimizar o efeito de distorções pontuais nos dados e o resultado foi registrado nos arquivos ```Weka/selecaoatributospm25.txt``` e ```Weka/selecaoatributospm10.txt``` para os campos PM2.5 e PM10 respectivamente.


Conforme estes resultados, o campo PM2.5 é relacionado principalmente aos seguintes campos:
* Dia da semana
* PM10
* CO
* Direção do vento
* Intensidade do vento


Já o campo PM10 é relacionado principalmente aos campos:
* Dia
* Hora
* PM2.5
* Chuva
* Estação de medição


### Existem padrões recorrentes nos dados?

A análise dos padrões recorrentes nos dados foi feita pela média, tanto geral quanto por estação. Os valores coletados foram gerados pelo programa ```recorrentes.py``` e tabulados nas planilhas ```mensais.ods```, ```dários.ods```, ```semanais.ods``` e ```porhora.ods``` da pasta ```python```. Nestes gráficos e tabelas é possível avaliar a evolução de cada um dos poluentes em cada estação e por cada métrica analisada, além da comparação das médias das estações com a média geral.


Em todas as dimensões analisadas (mensal, semanal, diário e por hora), foram encontrados ciclos relevantes. As medições de todas as estações seguiram quase sempre a tendência geral, subindo ou descendo conforme a média em grau similar em praticamente todas as situações. Em cada caso foi possível identificar algumas estações com valores sempre acima da média e outras com valores sempre abaixo. Os casos em que houve alguma diferenciação nas tendências são detalhados mais abaixo no item 5.


### Os dados seguem alguma tendência ao longo do período estudado?

A análise das tendências anuais foi feita pela média, tanto geral quanto por estação. Os valores coletados foram gerados pelo programa ```visual.py``` e tabulados na planilha ```python/anuais.ods```. Nestes gráficos é possível avaliar a evolução de cada um dos poluentes em cada estação, além da comparação deles com a média geral. O ano foi mantido conforme o padrão proposto pelos dados, de março do ano corrente até o último dia de fevereiro do ano seguinte. Manter os mesmos períodos em todos os anos permite uma comparação mais coerente.


No caso do PM2.5, as médias anuais indicam que em praticamente todas as estações (exceto Huairou) a tendência foi de queda de 2013 a 2015 e aumento entre 2015 e 2016.


No caso do PM10, as médias anuais indicam que em praticamente todas as estações (exceto Aotizhongxin) a tendência foi de queda comparando-se 2013 com 2015 e aumento entre 2015 e 2016.


### Considerando que são dados coletados em regiões próximas, existe correlação entre os valores obtidos nas diversas estações?

O Weka identificou a existência de uma correlação entre o vento e o poluente PM2.5 e também identificou que não há uma correlação significativa do vento com o poluente PM10. Também com identificada a correlação da chuva apenas com o poluente PM10, sendo que o poluente PM2.5 não demonstra ser influenciado significativamente pela ocorrência de chuva.


## 5. Explicação dos dados

### P2.5



### P10
