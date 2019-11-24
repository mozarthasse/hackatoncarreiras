#/bin/bash
cat PRSA_Data_20130301-20170228/* |grep -v station >juntoB.csv
echo No,year,month,day,hour,PM2.5,PM10,SO2,NO2,CO,O3,TEMP,PRES,DEWP,RAIN,wd,WSPM,station,,,,,,,, >juntoA.csv
cat juntoA.csv juntoB.csv >junto.csv
rm juntoA.csv
rm juntoB.csv
