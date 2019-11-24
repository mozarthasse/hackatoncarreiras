#/bin/bash
cat preprocessado.csv |grep -v station > pre.arff
sed -i 's/NA/?/g' pre.arff
cat cabecalho.arff pre.arff > entrada.arff
cat pre.arff |grep Aotizhongxin >pre1.arff
cat pre.arff |grep Changping >pre2.arff
cat pre.arff |grep Dingling >pre3.arff
cat pre.arff |grep Dongsi >pre4.arff
cat pre.arff |grep Guanyuan >pre5.arff
cat pre.arff |grep Gucheng >pre6.arff
cat pre.arff |grep Huairou >pre7.arff
cat pre.arff |grep Nongzhanguan >pre8.arff
cat pre.arff |grep Shunyi >pre9.arff
cat pre.arff |grep Tiantan >pre10.arff
cat pre.arff |grep Wanliu >pre11.arff
cat pre.arff |grep Wanshouxigong >pre12.arff
rm pre.arff
cat cabecalho.arff pre1.arff > entrada1.arff
cat cabecalho.arff pre2.arff > entrada2.arff
cat cabecalho.arff pre3.arff > entrada3.arff
cat cabecalho.arff pre4.arff > entrada4.arff
cat cabecalho.arff pre5.arff > entrada5.arff
cat cabecalho.arff pre6.arff > entrada6.arff
cat cabecalho.arff pre7.arff > entrada7.arff
cat cabecalho.arff pre8.arff > entrada8.arff
cat cabecalho.arff pre9.arff > entrada9.arff
cat cabecalho.arff pre10.arff > entrada10.arff
cat cabecalho.arff pre11.arff > entrada11.arff
cat cabecalho.arff pre12.arff > entrada12.arff

rm pre1.arff
rm pre2.arff
rm pre3.arff
rm pre4.arff
rm pre5.arff
rm pre6.arff
rm pre7.arff
rm pre8.arff
rm pre9.arff
rm pre10.arff
rm pre11.arff
rm pre12.arff
