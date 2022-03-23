from neuralNetwork import NeuralNetwork
import random
import numpy as np

class AntColonyOptmization:
    def __init__(self, colonySize, elitims, tau_inicial, alpha, rho_global, rho_local, update_gain, exploration_rate, maxparvalue, minparvalue, mesh, mutationRate, architecture):
        self.colonySize = colonySize
        self.elitims = elitims
        self.tau_inicial = tau_inicial
        self.alpha = alpha
        self.rho_global = rho_global
        self.rho_local = rho_local
        self.update_gain = update_gain
        self.exploration_rate = exploration_rate
        self.maxparvalue = maxparvalue
        self.minparvalue = minparvalue
        self.mesh = mesh
        self.mutationRate = mutationRate
        
        self.tau = tau_inicial*np.ones((self.maxparvalue-self.minparvalue))
    
        self.architecture = architecture
        self.BestGlobalFitness = 1
        self.BestGlobal = NeuralNetwork(self.architecture)
        self.BestCurrent = NeuralNetwork(self.architecture)
        self.ants = []

        for i in range(colonySize):
            self.ants.append(NeuralNetwork(self.architecture))

    def popSort(self,fitness):
        sortedAnts = []
        sortedFitness = []
        cost = np.array(fitness)
        sort_index = np.argsort(cost)

        for i in range(self.colonySize-1,-1,-1):
            sortedAnts.append(self.ants[sort_index[i]])
            sortedFitness.append(fitness[sort_index[i]])

        return sortedAnts, sortedFitness

    def clearDups(self):
        for i in range(len(self.ants)):
            net1 = self.ants[i]
            for j in range(i,len(self.ants)):
                net2 = self.ants[j]
                if net1 == net2:
                    k = random.choice(range(1,len(self.architecture)))
                    z = random.choice(range(self.architecture[k]))
                    y = random.choice(range(self.architecture[k-1]))
                    self.ants[j].getNetwork()[k-1][z][y] = (self.minparvalue + (self.maxparvalue - self.minparvalue)*random.random(0,1))/self.mesh

    def feasible(self):
        for i in range(len(self.ants)):
            for j in range(len(self.ants[i].getNetwork())):
                for k in range(len(self.ants[i].getNetwork()[j])):
                    for z in range(len(self.ants[i].getNetwork()[j][k])):
                        self.ants[i].getNetwork()[j][k][z] = np.max(np.array([self.ants[i].getNetwork()[j][k][z], self.minparvalue/self.mesh]))
                        self.ants[i].getNetwork()[j][k][z] = np.min(np.array([self.ants[i].getNetwork()[j][k][z], self.maxparvalue/self.mesh]))

    def mutation(self):
        for individual in self.ants:
            network = individual.getNetwork()
            for layer in network:
                for neuron in layer:
                    for i in range(len(neuron)):
                        if random.random() < self.mutationRate:
                            neuron[i] += random.gauss(0,np.std(neuron))

    def getPopulation(self):
        return self.ants

    def reproduction(self,fitness):
        # pheromone decay
        self.tau = (1 - self.rho_global) * self.tau

        # Use each solution to update the pheromone for each parameter value
        for i in range(1,len(self.ants)):
            cost = 1/fitness[i]
            for j in range(len(self.ants[i].getNetwork())):
                for k in range(len(self.ants[i].getNetwork()[j])):
                    for z in range(len(self.ants[i].getNetwork()[j][k])): 
                        index = int(np.floor(self.ants[i].getNetwork()[j][k][z]*self.mesh))
                        index = np.max(np.array([index, self.minparvalue]))
                        index = np.min(np.array([index, self.maxparvalue-1]))
                        if (cost < 10**(-12)):
                            self.tau[index - self.minparvalue] = np.max(self.tau)
                        else:
                            self.tau[index - self.minparvalue] += self.update_gain/cost
        
        # Use the probabilities to generate new solutions
        for i in range(self.elitims,len(self.ants)):
            for j in range(len(self.ants[i].getNetwork())):
                for k in range(len(self.ants[i].getNetwork()[j])):
                    for z in range(len(self.ants[i].getNetwork()[j][k])):
                        prob = self.tau**self.alpha
                        prob = prob/np.sum(prob)
                        maxIndexProb = np.argmax(prob)
                        maxProb = prob[maxIndexProb]
                        if random.uniform(0.0, 1.0) < self.exploration_rate:
                            selectIndex = maxIndexProb
                        else:
                            selectProb = prob[0]
                            selectIndex = 0
                            while selectProb < random.uniform(0.0, 1.0):
                                selectIndex += 1
                                if selectIndex >= self.maxparvalue - self.minparvalue:
                                    break
                                selectProb += prob[selectIndex]
                        self.ants[i].getNetwork()[j][k][z] = (self.minparvalue + selectIndex)/self.mesh
                        # local pheromone update
                        self.tau[selectIndex] = (1-self.rho_local)*self.tau[selectIndex]+ self.rho_local*self.tau_inicial

        self.feasible()
        self.mutation()

    def evolution(self,fitness):
        self.ants, fitness = self.popSort(fitness)
        if self.BestGlobalFitness < fitness[0]:
            self.BestGlobal = self.ants[0]
            self.BestGlobalFitness = fitness[0]

        self.clearDups
        self.reproduction(fitness.copy())