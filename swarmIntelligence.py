from neuralNetwork import NeuralNetwork
import random
import numpy as np

class SwarmIntelligence:
    def __init__(self, swarmSize, c1, c2, w, mutationRate, architecture):
        self.swarmSize = swarmSize
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.mutationRate = mutationRate
        self.architecture = architecture
        self.BestGlobalFitness = 1
        self.BestGlobal = NeuralNetwork(self.architecture)
        self.BestCurrent = NeuralNetwork(self.architecture)
        self.swarm = []
        for i in range(swarmSize):
            self.swarm.append(NeuralNetwork(architecture))

    def getPopulation(self):
        return self.swarm

    def mutation(self,swarm):
            for individual in swarm:
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
                    particle.getNetworkVel()[i][j][k] = particle.getNetworkVel()[i][j][k]*self.w + ((self.BestGlobal.getNetwork()[i][j][k] - particle.getNetwork()[i][j][k])*z2+(self.BestCurrent.getNetwork()[i][j][k] - particle.getNetwork()[i][j][k])*z1)
                    particle.getNetwork()[i][j][k] = particle.getNetwork()[i][j][k] + particle.getNetworkVel()[i][j][k]
        return particle
   

    def reproduction(self,fitness):
        newswarm = []
        index_max1 = 0
        for i in range(len(fitness)):
            if fitness[index_max1] < fitness[i]:
                index_max1 = i
        newswarm.append(self.swarm[index_max1])

        for i in range(len(self.BestCurrent.getNetwork())):
            for j in range(len(self.BestCurrent.getNetwork()[i])):
                for k in range(len(self.BestCurrent.getNetwork()[i][j])):
                    self.BestCurrent.getNetwork()[i][j][k] = self.swarm[index_max1].getNetwork()[i][j][k]


        if self.BestGlobalFitness < fitness[index_max1]:
            self.BestGlobalFitness = fitness[index_max1]
            for i in range(len(self.BestCurrent.getNetwork())):
                for j in range(len(self.BestCurrent.getNetwork()[i])):
                    for k in range(len(self.BestCurrent.getNetwork()[i][j])):
                        self.BestGlobal.getNetwork()[i][j][k] = self.BestCurrent.getNetwork()[i][j][k]

 

        for i in range(len(self.swarm)):
            updatedParticle = self.update(self.swarm[i])
            newswarm.append(updatedParticle)

        #Optional
        self.mutation(newswarm)
        
        return newswarm

    def evolution(self,fitness):
        self.swarm = self.reproduction(fitness.copy())






