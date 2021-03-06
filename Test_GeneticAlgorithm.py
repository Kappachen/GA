# -*- coding: utf-8 -*-
import numpy
import ga
# import cost_ga
# from random import choice
import math
import random

def Performance_GA(data_size, ceph_sw, ceph_sr):
    # Inputs of the equation.
    equation_inputs_data = data_size # 資料大小[3.61]
    equation_inputs_sw = ceph_sw   # 資料寫入速度[47.3983503]
    equation_inputs_sr = ceph_sr    # 資料讀取速度[79.1313117]

    # Number of the weights we are looking to optimize.
    num_weights = 1



    """
    Genetic algorithm parameters:
        Mating pool size
        Population size
    """
    sol_per_pop = 12
    num_parents_mating = 6

    # Defining the population size.
    pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    # Creating the initial population.
    n = 8 # total OSD
    l = [1.5] # 安全性weight 1, 1.5, 2

    k = numpy.random.randint(low=2, high=n, size=pop_size) # 隨機產生抹除碼k值
    m = numpy.random.randint(low=1, high=4, size=pop_size) # 隨機獲取可靠性(M)基因
    ew = numpy.random.choice(l, size=pop_size) # 隨機獲取安全性基因

    # 檢測並產生人口
    new_population = ga.gene_detect(numpy.hstack([k,m,ew]), n, sol_per_pop)

    best_outputs = 99999999999
    best_solutions = []
    history_best = []
    num_generations = 10
    for generation in range(num_generations):
        # print("--------------------------------------------------------")
        print("==========================Generation : ", generation)
        print("pop")
        print(new_population)
        # Measuring the fitness of each chromosome in the population.
        fitness = ga.cal_pop_fitness(equation_inputs_data, equation_inputs_sw, equation_inputs_sr, new_population, pop_size, sol_per_pop)
        # cost_fitness = ga.cal_cost_fitness(equation_inputs_data, ci, ni, new_population, pop_size, sol_per_pop)
        print("Fitness")
        print(fitness)

        history_best.append(numpy.min(fitness))

        if best_outputs > numpy.min(fitness):
            best_outputs = numpy.min(fitness)
            best_solutionsinx = numpy.where(fitness == best_outputs)
            best_solutions = new_population[best_solutionsinx, :]
            # The best result in the current iteration.
            print (best_solutions)
            print("Best result : ", numpy.min(fitness))

        # Selecting the best parents in the population for mating.
        # 效能最佳化的parents
        parents = ga.roulette_wheel_select_mating_pool(new_population, fitness,
                                        num_parents_mating)
        print("Parents")
        print(parents)

        # Generating next generation using crossover.
        # 效能最佳化的crossover
        offspring_crossover = ga.crossover(parents,
                                        offspring_size=(pop_size[0]-parents.shape[0], 3))
        ga.gene_detect(offspring_crossover, n, num_parents_mating)
        print("Crossover")
        print(offspring_crossover)

        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_crossover

        # population_for_mutation = numpy.empty((pop_size[0],3))
        # population_for_mutation[0:parents.shape[0], :] = parents
        # population_for_mutation[parents.shape[0]:, :] = offspring_crossover

        # Adding some variations to the offspring using mutation.
        # if (math.floor(random.random() * 100) < 10) :
            # offspring_mutation = ga.mutation(population_for_mutation, n, num_mutations=2)
        offspring_mutation = ga.mutation(new_population, n, l, num_mutations=2)
        ga.gene_detect(offspring_mutation, n, sol_per_pop)
        print("Mutation")
        print(offspring_mutation)
            # Creating the new population based on the parents and offspring.
        new_population[:,:]=offspring_mutation


    # Getting the best solution after iterating finishing all generations.
    #At first, the fitness is calculated for each solution in the final generation.
    fitness = ga.cal_pop_fitness(equation_inputs_data, equation_inputs_sw, equation_inputs_sr, new_population, pop_size, sol_per_pop)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = numpy.where(fitness == numpy.min(fitness))

    # print("Best solution : ", new_population[best_match_idx, :])
    # print("Best solution fitness : ", fitness[best_match_idx])
    print ("best solution",best_solutions)
    print ('GA complete')
    return best_solutions[0,0]
    # print("best outputs", best_outputs)
    # print("history fitness", min(history_best))


    # import matplotlib.pyplot
    # matplotlib.pyplot.plot(history_best)
    # matplotlib.pyplot.xlabel("Iteration")
    # matplotlib.pyplot.ylabel("Fitness")
    # matplotlib.pyplot.show()
