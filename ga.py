# -*- coding: utf-8 -*-
import numpy
from operator import itemgetter
import random

def gene_detect(pop, n, pop_num):
    # 檢測基因是否符合比例
    for i in range (pop_num):
        x = n - pop[i, 0] # pop[i,0] = k
        if (pop[i, 0] >= n-1 or pop[i, 0] == 2): # k >= 7 or k = 2
            pop[i, 1] = 1 # 設定m=1
        elif (pop[i, 0] == pop[i, 1]): # k == m
            pop[i, 1] = numpy.random.randint(low=1, high=pop[i, 0]) # 設定m < k
        elif (pop[i, 0]+pop[i, 1] > n): # k+m > n
            pop[i, 1] = numpy.random.randint(low=1, high=x+1) # 設定m<n
    return pop

def cost_gene_create(pop,pop_num,pop_size,cost):
    # 根據傳入的抹除碼k,m值產生基因變數ni
    last_ni = []
    last_cost = []
    for i in range(pop_num):
        ni_l= []
        cost_l = []
        n = pop[i, 0:1]+pop[i, 1:2]
        while n > 0 :
            for x in range(int(n)):
                ni = random.randint(0, n)
                ci = random.choice(cost)
                ni_l.append(ni)
                cost_l.append(ci)
                n -= ni
        last_ni.append(ni_l)
        last_cost.append(cost_l)
    return last_ni, last_cost


def cal_pop_fitness(data, sw, sr, pop,pop_size,pop_num):
    # 效能考量的儲存策略
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    k = numpy.empty(pop_size)
    m = numpy.empty(pop_size)
    n = numpy.empty(pop_size)
    ew = numpy.empty(pop_size)
    for i in range(pop_num):
        k[i,0] = pop[i, 0:1]
        m[i,0] = pop[i, 1:2]
        n[i,0] = pop[i, 0:1]+pop[i, 1:2]
        ew[i,0] = pop[i, 2:3]
    time = numpy.multiply(numpy.divide(data, k), n)
    tu = numpy.divide(time, sw)
    td = numpy.divide(time, sr)
    Rw = numpy.multiply(m, m)
    # fitness = numpy.sum(tu+td, axis=1)
    fitness = numpy.divide(numpy.divide(numpy.sum(tu+td, axis=1), numpy.hstack(ew)), numpy.hstack(Rw))
    return fitness

def cal_cost_fitness(data, cost, num_ni, pop, pop_size,pop_num):
    # 成本考量的儲存策略
    k = numpy.empty(pop_size)
    m = numpy.empty(pop_size)
    n = numpy.empty(pop_size)
    ew = numpy.empty(pop_size)
    totoal_cost = []
    sum_cost = numpy.empty(pop_size)
    for i in range(pop_num):
        k[i,0] = pop[i, 0:1]
        m[i,0] = pop[i, 1:2]
        n[i,0] = pop[i, 0:1]+pop[i, 1:2]
        totoal_cost.append([(x[0]*x[1]) for x in zip(num_ni[i],cost[i])]) #ni*ci
        ew[i,0] = pop[i, 2:3]
    data_slice = numpy.divide(data, k) #data/k
    # print("ci = ", totoal_cost)
    # print(data_slice)
    for i in range(pop_num):
        # 加總所有儲存裝置的儲存成本
        x = numpy.multiply(data_slice[i],totoal_cost[i]) #(data/k)*ni*ci
        sum_cost[i,0] = x.sum()
    # print("sum_cost = ", sum_cost)
    Rw = numpy.multiply(m, m)
    fitness = numpy.divide(numpy.divide(sum_cost, ew), Rw)
    return fitness

def roulette_wheel_select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    Sfitness = numpy.divide(1, fitness) # 選取適應值小的，故將適應值取倒數
    choose_Sfitness = sorted(Sfitness)
    # sum_fitness = sum(choose_Sfitness) # 全部fitness總和
    # probability = numpy.divide(choose_Sfitness,sum_fitness)
    select_fitnum = []
    parents = numpy.empty((num_parents, pop.shape[1]))
    while len(select_fitnum) < num_parents:
        i = len(select_fitnum)
        randNum = random.random() #0~1 中隨機取得的亂數
        partialSum = 0 # 目前的機率加總
        for ind in choose_Sfitness:
            partialSum += ind
            # print("partialSum",partialSum)
            if partialSum >= randNum:
                #when the sum of 1/fitness is bigger than u, choose the one, which means u is in the range of [sum(1,2,...,n-1),sum(1,2,...,n)] and is time to choose the one ,namely n-th individual in the pop
                select_fitnum.append(ind)
                min_fitness_idx = numpy.where(ind == Sfitness)
                min_fitness_idx = min_fitness_idx[0][0]
                parents[i, :] = pop[min_fitness_idx, :]
                break
    return parents

def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover, n, l, num_mutations=1):
    mutations_counter = numpy.uint8(offspring_crossover.shape[1] / num_mutations)
    # Mutation changes a number of genes as defined by the num_mutations argument. The changes are random.
    for idx in range(offspring_crossover.shape[0]):
        gene_idx = mutations_counter - 1
        for mutation_num in range(num_mutations):
            # The random value to be added to the gene.
            random_value = numpy.random.randint(low=2, high=n)
            offspring_crossover[idx, gene_idx] =  random_value
            offspring_crossover[idx, gene_idx+1] =  numpy.random.randint(low=1,high=4)
            offspring_crossover[idx, gene_idx+2] =  numpy.random.choice(l)
            if (offspring_crossover[idx, gene_idx+1] >= offspring_crossover[idx, gene_idx]):
                offspring_crossover[idx, gene_idx+1] = numpy.random.randint(low=1, high=offspring_crossover[idx, gene_idx])
            # gene_idx = gene_idx + mutations_counter
    return offspring_crossover


# def cal_pop_fitness(data, sw, sr, k, n, ew, m):
#     # Calculating the fitness value of each solution in the current population.
#     # The fitness function calulates the sum of products between each input and its corresponding weight.
#     time = numpy.multiply(numpy.divide(data, k), n)
#     tu = numpy.divide(time, sw)
#     td = numpy.divide(time, sr)
#     Rw = numpy.multiply(m, m)
#     # fitness = numpy.sum(tu+td, axis=1)
#     fitness = numpy.divide(numpy.divide(numpy.sum(tu+td, axis=1), numpy.hstack(ew)), numpy.hstack(Rw))
#     return fitness

# def select_mating_pool(pop, fitness, num_parents):
#     # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
#     parents = numpy.empty((num_parents, pop.shape[1]))
#     for parent_num in range(num_parents):
#         min_fitness_idx = numpy.where(fitness == numpy.min(fitness))
#         min_fitness_idx = min_fitness_idx[0][0]
#         parents[parent_num, :] = pop[min_fitness_idx, :]
#         fitness[min_fitness_idx] = 99999999999
#     return parents

# def cal_km(k, m, n, pop_size, pop_num):
#     # 檢驗抹除碼是否符合參數m小於k且m+k小於n
#     # m = numpy.random.randint(low=1, high=4, size=pop_size) # 隨機獲取可靠性(M)基因
#     for i in range (pop_num):
#         x = n - k[i]
#         if (x <= [1]):
#             m[i] = 1
#         elif (k[i]+m[i] >= n):
#             m[i] = numpy.random.randint(low=1, high=x)