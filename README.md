# GeneticAlgorithmPython

Genetic algorithm implementation in Python

## 執行流程簡述
readfilesize 取得資料大小＆使用者決策，
並透過Test_GeneticAlgorithm或是costTest得到效能、成本的最佳部署方法，
最後建立ECP並將計算結果部署到Ceph中

## 使用方法
python readfilesize.py -i " 欲儲存之資料 " -s " 使用效能（1）或成本（0）最佳化 "   
當 user 選擇 1 時執行 Test_GeneticAlgorithm.py   
相反的當 user 選擇 0 時執行 costTest.py   
Test_GeneticAlgorithm.py & costTest.py 裡的基因演算法皆透過 ga.py 執行 

## 開發背景（學長研究動機）
學長論文（基於Ceph物件式儲存系統結合資料壓縮技術之研究）透過 Ceph ，並使用抹除碼及結合資料壓縮技術。
透過資料壓縮技術以及抹除碼來減少儲存空間的使用，並考慮到***每個檔案的特性***(如檔案大小、讀取和寫入的比例)，***來配合不同的抹除碼配置***，並且對資料進行加密的動作，讓使用者能夠擁有一定的安全性傳輸。

## 問題分析
目前尚未有能根據使用者需求，且考慮每個檔案之特性，去自動配置最佳儲存方案的元件

## 已完成進度
僅提供使用者輸入儲存策略，並依據 GA 演算法所得出之最佳抹除碼配置去建立 Erasure Code Pool

## 待開發
* 提供使用者輸入對上傳時間、下載時間、或是安全性等方面的條件限制要求（目前僅能在 Cost_GA 或 Performance_GA 兩函數中手動設定參數）  
* 部署時實際上尚未對儲存之檔案做加密（安全性）

# 論文相關
## 問題分析
這個研究方法的優點？多目標最佳化問題是什麼？（學長的類似問題的分析，不用其推導過程只講結論）並證明此問題是np hard(多目標最佳化np hard問題的證明)，無法在有效時間內求得最佳解，因此他是一個多目標問題所以採用ＧＡ來解決，接下來講如何設計ＧＡ來map最佳解。

# 未完成
系統架構圖
