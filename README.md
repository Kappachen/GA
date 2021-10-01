# GeneticAlgorithmPython

Genetic algorithm implementation in Python

## 流程
readfilesize 取得資料大小＆使用者決策，
並透過Test_GeneticAlgorithm或是costTest得到效能、成本的最佳部署方法，
最後建立ECP並將計算結果部署到Ceph中

## 使用方法
python readfilesize.py -i " 欲儲存之資料 " -s " 使用效能（1）或成本（0）最佳化 "   
當 user 選擇 1 時執行 Test_GeneticAlgorithm.py   
相反的當 user 選擇 0 時執行 costTest.py   
Test_GeneticAlgorithm.py & costTest.py 裡的基因演算法皆透過 ga.py 執行  
