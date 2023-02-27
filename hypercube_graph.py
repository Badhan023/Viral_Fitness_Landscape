import sys
import logging
import random

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    
# Creating an object
logger = logging.getLogger()
    
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

def calculate_fitness(genotype):
    #straightforward fitness assignment depending on the count of 1's in the genotype
    count = genotype.count('1')
    fitness=count/len(genotype)
    
    return fitness

def generate_all_binary_strings(n, arr, i, list):

    if i==n:
        st=""
        for i in range(0, n):
            st+=str(arr[i])
        
        list.append(st)
        return
    
    arr[i]=0
    generate_all_binary_strings(n, arr, i + 1, list)
    arr[i]=1
    generate_all_binary_strings(n, arr, i + 1, list)
    


class node:
    genotype=""
    fitness=0
    transmissibility=0

    def __init__(self, genotype, fitness):
        self.genotype=genotype
        self.fitness=fitness
        
    def get_fitness(self):              #returns the fitness value
        return self.fitness
    
    def get_genotype(self):
        return self.genotype      
        
    

class hypercube:
    base=0                  #binary
    n=0
    node_list={}            #V
    adjacency_list={}       #this is a dictionary keeping the adjacency list
    strain_list=[]

    def __init__(self, base, n):
        self.base=base
        self.n=n

    def print_hypercube(self):
        for node in self.adjacency_list:
            logger.info("node : "+ str(node) + "(" + str(self.get_fitness(node)) + ")" + " neighbors : " + str(self.get_neighbors(node)))
            
        
    def get_all_vertices(self):
        list=[]         #list of genotypes
        arr = [None]*self.n
        generate_all_binary_strings(self.n, arr, 0, list)
        #print (list)
        self.strain_list=list
        
        for genotype in list:
            count = genotype.count('1')
            
            fitness=calculate_fitness(genotype)
            #print (fitness)
            logger.info("genotype: " + genotype + ",fitness: " + str(fitness))
            self.node_list[genotype] = node(genotype, fitness)
    
    def get_strains(self):
        return self.strain_list

    def build_hypercube(self):
        for v in self.node_list:
            
            self.adjacency_list[v]=[]
            for i in range(0, int(sys.argv[1])):
                if self.node_list[v].genotype[i]=='1':
                    temp = list(self.node_list[v].genotype)
                    temp[i] = '0'
                    
                else:
                    temp = list(self.node_list[v].genotype)
                    temp[i] = '1'
                    
                neighbor_genotype = "".join(temp)
                neighbor_fitness = calculate_fitness(neighbor_genotype)        #calculating fitness
                neighbor = node(neighbor_genotype, neighbor_fitness)
                self.adjacency_list[v].append(neighbor)
            #print (self.adjacency_list[v])

    def get_neighbors(self, v):
        neighbors_list={}
        for i in range(int(sys.argv[1])):
            neighbors_list[self.adjacency_list[v][i].get_genotype()] = self.adjacency_list[v][i].get_fitness()
        return neighbors_list

    def get_fitness(self, genotype):
        #print (self.node_list[genotype].fitness)
        return self.node_list[genotype].fitness
    
    def get_fittest_state(self):
        max_fit = -1
        fittest_state = ""
        for i in self.node_list:
            if self.node_list[i].get_fitness() > max_fit:
                max_fit = self.node_list[i].get_fitness()
                fittest_state = self.node_list[i].get_genotype()
        return fittest_state

    def get_least_fit_state(self):
        min_fit = 1000
        least_fit_state = ""
        for i in self.node_list:
            if self.node_list[i].get_fitness() < min_fit:
                min_fit = self.node_list[i].get_fitness()
                least_fit_state = self.node_list[i].get_genotype()
        return least_fit_state
 
bit = sys.argv[1]



