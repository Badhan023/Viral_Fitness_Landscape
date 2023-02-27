# Viral_Fitness_Landscape

To understand the evolutionary causes and consequences, evolutionary biologists study the genotype-fitness map, also known as fitness landscape. Fitness landscapes provide information on molecuar and evolutionary constraints by formalizing the relationship between genotype or phenotype and fitness

This project has combined two models: the fitness model and the network model. The network model has been implemented by the [Waxman graph](https://networkx.org/documentation/stable/reference/generated/networkx.generators.geometric.waxman_graph.html). The adaptive walk in the fitness landscape has been modeled by modifying the [Simulated Annealing](https://www.sciencedirect.com/science/article/pii/B9780081010419000028) algorithm. 
The [waxman_model.py](waxman_model.py) is the network model and the [hypercube_graph.py](hypercube_graph.py) is the fitness model.
