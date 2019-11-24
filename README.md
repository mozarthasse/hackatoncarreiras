# hackatoncarreiras
Trabalho para o hackaton de carreiras

#1. Questões de pesquisa e justificativas:

* Qual a amplitude e variação nos valores dos campos?
- necessário para verificar a integridade dos dados e para tirar conclusões mais evidentes ou que possam direcionar os passos seguintes na pesquisa.

* Existem correlações fortes ou evidentes entre os campos?
- descobrir e/ou eliminar as conclusões mais triviais antes de tentar mecanismos mais elaborados de análise.

* Existem padrões recorrentes nos dados?
- Buscar por padrões cíclicos que expliquem a maior parte da variação nos valores e permita alguma previsibilidade a curto prazo. As hipóteses mais óbvias a analisar consistem em identificar a presença ou ausência de padrões:
-- anuais
-- mensais
-- semanais
-- diários

* Os dados seguem alguma tendência ao longo do período estudado?
- verificar se há alguma indicação de que os índices estão subindo ou descendo a longo prazo.

* Considerando que são dados coletados em regiões próximas, existe correlação entre os valores obtidos nas diversas estações?
- verificar se há efeito mensurável na difusão dos poluentes em função da proximidade entre as estações.


#2. Ferramentas usadas

- Linux Ubuntu: software livre base para uso de todos os outros, incluindo o bash para o processamento trivial de arquivos.

- Libreoffice Calc: colocar fórmulas numa planilha ajuda no processamento mais trivial como a criação de campos complementares em formato adequado para análise.

- Weka: a disponibilidade de algoritmos de inteligência artifical, mineração de dados e ferramentas de tratamento básicos dos dados são convenientes para responder perguntas que porventura surjam durante a análise.

- Python: linguagem prática e rápida para transformar em imagens os dados e ajudar no direcionamento da análise.


#3. Tratamento dos dados e métodos usados

3.1. Junção dos dados em um único arquivo CSV com todos os campos tratados

Resumo macro:
  PRSA_Data_20130301-20170228 + junta.sh => junto.csv
  junto.csv => preprocessamento.ods
  preprocessamento.ods => preprocessado.csv + cabecalho.arff

Decidiu-se juntar os dados de todas as estações em um único arquivo para facilitar o processamento via planilha. Usou-se para isso o arquivo "junta.sh", que transforma todos os arquivos em um único chamado "junto.csv"

Depois, abre-se o arquivo "junto.csv" pelo LibreOffice, tomando o cuidado de interpretar os campos numéricos no formato Inglês (ponto decimal ao invés de vírgula).

Os campos criados na planilha foram:
- dia da semana: valor de 1 a 7 deduzido dos campos "year", "month", "day".
- dia normalizado: campo para tratar a data como sendo um valor numérico contínuo.Considera como fração o número de horas desde o começo do ano até o dia e hora da medição. Pode ser mais conveniente para identificar correlações ou fazer previsões sazonais.
- ângulo do vento: transforma o campo texto em um valor numérico para facilitar a eventual busca de correlações entre o grau de poluição da estação pesquisada e a vizinhança caso o vento seja identificado como fator relevante.
- latitude e longitude: posição APROXIMADA de cada estação para que se possa oportunamente medir distâncias entre elas e analisar mais a fundo a contribuição do vento para carregar a poluição entre estações próximas. Não foi encontrada a localização EXATA, porém é possível deduzir as coordenadas GPS fazendo uma regra-de-três entre os gráficos exibidos em artigos que já analisaram esta base de dados e as coordenadas GPS de dois pontos no mapa seja razoavelmente conhecida. Mesmo reconhecidamente inadequada para tirar conclusões impecáveis sobre essas correlações, esta aproximação já ajuda BASTANTE a representar visualmente o comportamento dos dados.

Todos estes campos e suas fórmulas estão no arquivo "preprocessamento.ods". Ele deve ser transformado novamente em csv
selecionando-se a primeira planilha do arquivo e mandando salvá-la como "preprocessado.csv". NÃO colocar aspas em todas as células de texto e mandar salvar o conteúdo das células como mostrado para preservar o ponto decimal e número de casas decimais.

3.2. Preparação para uso do Weka

Resumo macro:
  junta2.sh + cabecalho.arff + preprocessado.csv => entrada*.arff

O formato weka é praticamente igual ao csv, sendo necessário apenas acrescentar um cabeçalho (arquivo "cabecalho.arff" gerado a partir do "preprocessamento.ods").
A conversão de csv para arff foi feita através da execução do arquivo "junta2.sh". Neste arquivo foram feitas versões separadas das estações ("entrada1.arff" a "entrada12.arff") para que se possa oportunamente usar o pacote de análise de séries temporais.


#4. Resultados coletados


#5. Conclusões
