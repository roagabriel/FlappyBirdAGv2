from neuralNetwork import NeuralNetwork
import random
import numpy as np

class PSO:
    def __init__(self, populationSize, c1, c2, mutationRate, architecture):
        self.populationSize = populationSize
        self.c1 = c1
        self.c2 = c2
        self.mutationRate = mutationRate
        self.architecture = architecture
        self.BestGlobalFitness = -1
        self.BestGlobal = NeuralNetwork(self.architecture)
        self.BestCurrent = NeuralNetwork(self.architecture)
        self.population = []
        for i in range(populationSize):
            self.population.append(NeuralNetwork(architecture))

    def getPopulation(self):
        return self.population

    def mutation(self,population):
            for individual in population:
                network = individual.getNetwork()
                for layer in network:
                    for neuron in layer:
                        for i in range(len(neuron)):
                            if random.random() < self.mutationRate:
                                neuron[i] += random.gauss(0,np.std(neuron))

    def update(self, particle):
        z1 = self.c1*random.uniform(0.0, 1.0)
        z2 = self.c2*random.uniform(0.0, 1.0)
        for i in range(len(particle.getNetwork())):
            for j in range(len(particle.getNetwork()[i])):
                for k in range(len(particle.getNetwork()[i][j])):
                    particle.getNetwork()[i][j][k] = particle.getNetwork()[i][j][k] + ((self.BestGlobal.getNetwork()[i][j][k] - particle.getNetwork()[i][j][k])*z2+(self.BestCurrent.getNetwork()[i][j][k] - particle.getNetwork()[i][j][k])*z1)
        return particle
   

    def reproduction(self,fitness):
        newPopulation = []
        index_max1 = 0
        for i in range(len(fitness)):
            if fitness[index_max1] < fitness[i]:
                index_max1 = i
        newPopulation.append(self.population[index_max1])

        for i in range(len(self.BestCurrent.getNetwork())):
            for j in range(len(self.BestCurrent.getNetwork()[i])):
                for k in range(len(self.BestCurrent.getNetwork()[i][j])):
                    self.BestCurrent.getNetwork()[i][j][k] = self.population[index_max1].getNetwork()[i][j][k]


        if self.BestGlobalFitness < fitness[index_max1]:
            self.BestGlobalFitness = fitness[index_max1]
            for i in range(len(self.BestCurrent.getNetwork())):
                for j in range(len(self.BestCurrent.getNetwork()[i])):
                    for k in range(len(self.BestCurrent.getNetwork()[i][j])):
                        self.BestGlobal.getNetwork()[i][j][k] = self.BestCurrent.getNetwork()[i][j][k]

 

        for i in range(1,len(self.population)):
            updatedParticle = self.update(self.population[i])
            newPopulation.append(updatedParticle)

        #Optional
        self.mutation(newPopulation)
        
        return newPopulation

    def evolution(self,fitness):
        self.population = self.reproduction(fitness.copy())






