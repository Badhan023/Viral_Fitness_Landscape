# Viral_Fitness_Landscape

To understand the evolutionary causes and consequences, evolutionary biologists study the genotype-fitness map, also known as fitness landscape. Fitness landscapes provide information on molecuar and evolutionary constraints by formalizing the relationship between genotype or phenotype and fitness

This project has combined two models: the fitness model and the network model. The network model has been implemented by the [Waxman graph](https://networkx.org/documentation/stable/reference/generated/networkx.generators.geometric.waxman_graph.html). The adaptive walk in the fitness landscape has been modeled by modifying the [Simulated Annealing](https://www.sciencedirect.com/science/article/pii/B9780081010419000028) algorithm. 
The [waxman_model.py](waxman_model.py) is the network model and the [hypercube_graph.py](hypercube_graph.py) is the fitness model.

## Create conda environment
```hs
conda env create -f environment.yml
conda activate virafit
```

## Verify installation
While running the code, be in the Viral_Fitness_Landscape folder.
```hs
python waxman_model.py 5 100 0.25 5 0.5 bin
```
Expected output includes:
```hs
Mean adaptive walk: <value>
Std dev: <value>
N: 100
```

## Running the simulation
```hs
python3 waxman_model.py <sequence_length> <network_size> <mutation_rate> <duration> <infection_probability> <sequence_type> 
```
Here, sequence_length = length of the viral genome sequence

network_size = size of the network in the Waxman model

mutation_rate = the mutation rate of the infecting virus

duration = the infection duration of an infection in the body of a host

infection_probability = the probability of an uninfected host being infected

sequence_type = bin / nucl
