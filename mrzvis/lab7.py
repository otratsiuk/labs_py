import math
import random

import numpy as np

servers_num = 10
population_size = 30
chromosome_length = 8
gene_is_missing = 1000
elitism_num = 10 

iteratons = input('Enter num of iterations: ')
mutation_percent = input('Enter mutation percent(float): ')


matrix = np.loadtxt('/home/volga/Git/labs_py/mrzvis/matrix.csv', dtype = int)
print(matrix)


def init_first_population(sender, reciever): 
    population = []

    for individual in range(population_size):
        chromosome = []
        for gene in range(chromosome_length):
            chromosome.append(random.randint(0, chromosome_length + 1))

        chromosome[0] = int(sender)
        chromosome[chromosome_length - 1] = int(reciever)    
        population.append(chromosome)

    return population    


def most_similar(chromosome, population):
    shortest_hamming_distance = chromosome_length
    curr_hamming_distance = 0
    similar = chromosome

    for individual in population:
        curr_hamming_distance = 0
        for i in range(chromosome_length):
            if individual[i] != chromosome[i]:
                curr_hamming_distance += 1

        if curr_hamming_distance < shortest_hamming_distance and curr_hamming_distance != 0:
            shortest_hamming_distance = curr_hamming_distance
            similar = individual

    return similar        

def fitness_function(population):
    fitness = []
    for chromosome in population:
        fit = 0
        j = 1
        for i in range(chromosome_length - 1):
            while(j < chromosome_length and chromosome[j] == gene_is_missing):
                j += 1
            if(chromosome[i] != gene_is_missing and j < chromosome_length):
                fit += matrix[chromosome[i]][chromosome[j]]
                j += 1    
        fitness.append(fit)   

    return fitness    

def distance(chromosome):
    fit = 0
    j = 1
    for i in range(chromosome_length - 1):
        while(j < chromosome_length and chromosome[j] == gene_is_missing):
            j += 1
        if(chromosome[i] != gene_is_missing and j < chromosome_length):
            fit += matrix[chromosome[i]][chromosome[j]]
            j += 1

    return fit        

def best_fitness(fitness):
    best = 1000
    for fit in fitness:
        if fit < best:
            best = fit

    return best  

def next_best_fitness(fitness, prev_best):
    best = 1000
    for fit in range(len(fitness)):
        if fitness[fit] < best and fitness[fit] > fitness[prev_best] and fit != prev_best:
            best = fitness[fit]

    return best 

def solution_pos(population):
    fitness = fitness_function(population)
    best = best_fitness(fitness)

    for i in range(population_size):
        if fitness[i] == best:
            return i


def elitism_selection(population):
    fitness = fitness_function(population)
    best = best_fitness(fitness)
    best_individuals = []

    for i in range(int(elitism_num)):
        for fit in range(len(fitness)):
            if fitness[fit] == best:
                best_individuals.append(population[fit])
                best = next_best_fitness(fitness, fit)
                break

    return best_individuals            



def two_point_crossover(first_parent, second_parent):
    first_point = random.randint(1, chromosome_length)
    second_point = random.randint(1, chromosome_length)

    while(second_point == first_point):
        second_point = random.randint(1, chromosome_length)

    if(first_point > second_point):
        first_point, second_point = second_point, first_point

    first_child = first_parent
    second_child = second_parent
    for gene in range(first_point, second_point):
        first_child[gene] = second_parent[gene]
        second_child[gene] = first_parent[gene]

    first_child = mutation(first_child)
    second_child = mutation(second_child)    

    return first_child, second_child    



def mutation(child):
    possibility = random.randint(0, 100)
    if possibility <= float(mutation_percent) * 100:
        gene_pos = random.randint(1, chromosome_length - 2)

        if child[gene_pos] == gene_is_missing:
            gene = random.randint(0, servers_num - 1)
            child[gene_pos] = gene
        else:
            child[gene_pos] = gene_is_missing

    return child        



def inbreeding(population):
    i = 0
    next_population = []

    while i < (len(population) - int(elitism_num)) / 2:
        i += 1
        index = random.randint(0, len(population) - 1)

        first_parent = population[index]
        second_parent = most_similar(first_parent, population)

        children = two_point_crossover(first_parent, second_parent)

        next_population.append(children[0])
        next_population.append(children[1])

    reproducted_individuals = elitism_selection(population)

    next_population.extend(reproducted_individuals)    

    return next_population    


def find_solution(initial_population):
    best_chromosome = []
    best_distance = 1000

    for i in range(int(iteratons)):
        next_population = inbreeding(initial_population)

        print('\nnext population: ')
        for rows in next_population:
            print(rows)

        fitness = fitness_function(next_population)
        best_in_population = best_fitness(fitness)
        
        pos = solution_pos(next_population)
        solution_chromosome = next_population[pos]

        print('\nsolution for population: ')
        print(solution_chromosome)

        print("solution distance: ")
        print(best_in_population)


        if best_in_population <= best_distance:
            best_distance = best_in_population
            best_chromosome = solution_chromosome   

    return best_chromosome       

def print_solution(solution):
    prev = solution[0]
    line = str(prev)
    for i in range(1, len(solution)):
        if(solution[i] != prev and solution[i] != gene_is_missing):
            line += ' -> ' + str(solution[i])
            prev = solution[i]   
    print(line)


sender = input('Enter sender: ')
reciever = input('Enter reciever: ')

initial_population = init_first_population(sender, reciever)
print("\ninitial population: ")
for rows in  initial_population:
    print(rows)

solution = find_solution(initial_population)
print('\nfinal solution: ')
print_solution(solution)


print("solution distance: ")
print(distance(solution))
