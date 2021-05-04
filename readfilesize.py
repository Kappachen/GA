#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import getsize
import Test_GeneticAlgorithm
import costTest
import sys, getopt
import os

def main(argv):
   inputfile = ''
   Ec_results = ''
   try:
      opts, args = getopt.getopt(argv,"hi:s:",["help","ifile","strategy="])
   except getopt.GetoptError:
      print ('readfilesize.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
            print('readfilesize.py -i <inputfile>')
            sys.exit()
       elif opt in ('-i', '--ifle'):
            inputfile = arg
            size = getsize(inputfile)
       elif opt in ('-s', '--strategy'):
            strategy = arg
   print ('inputfile name :', inputfile)
   print ('file size :', size)    #取得資料大小（bytes）
   print ('user_stategy : ', strategy) #獲取使用者決策
   if strategy == '1' :
        Ec_results = Test_GeneticAlgorithm.Performance_GA(size, 47.3983503, 79.1313117) #效能
   elif strategy == '0' :
        Ec_results = costTest.Cost_GA(size) #成本
   else :
        print('輸入有誤')
   print(Ec_results)
   k = Ec_results[0]
   m = Ec_results[1]
   # 將計算結果部署到ceph中
    # 建立ECP
   os.system("ceph osd erasure-code-profile set myprofile k=%d m=%d crush-failure-domain=rack" % (k,m))
    # # 建立一個自己設定的profile
   os.system("ceph osd pool create ecpool 12 12 erasure <myprofile>")


if __name__ == "__main__":
   main(sys.argv[1:])

    # 將計算結果部署到ceph中
    # 建立ECP
    # ceph osd erasure-code-profile set myprofile k=3 m=2 ruleset-failure-domain=rack
    # # 建立一個自己設定的profile
    # ceph osd pool create ecpool 12 12 erasure <myprofile>

#%%
# data = pd.read_csv("data/EightJobs.csv")
# jap = JAPProblem(data.values)
# jap.compute_objective_value(range(len(data)))

# pop_size = 50
# selection_type = SelectionType.Deterministic
# crossover_type = CrossoverType.PartialMappedCrossover
# crossover_rate = 0.2
# mutation_type = MutationType.Inversion
# mutation_rate = 0.1
# solver = GeneticAlgorithm(pop_size,jap.number_of_jobs,selection_type,
#                           crossover_type,crossover_rate,
#                           mutation_type,mutation_rate,
#                           jap.compute_objective_value)
# solver.initialize()

# for i in range(100):
#     solver.perform_crossover_operation()
#     solver.perform_mutation_operation()
#     solver.evaluate_fitness()
#     solver.update_best_solution()
#     solver.perform_selection()
#     if(i %10 ==0):
#         print(F"iteration {i} :")
#         print(f"{solver.best_chromosome}: {jap.compute_objective_value(solver.best_chromosome)}")