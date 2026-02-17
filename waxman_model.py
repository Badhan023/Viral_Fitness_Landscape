import hypercube_graph as hg
import networkx as nx
import pandas as pd
import math
import sys
import random
import logging
from itertools import combinations
import numpy as np

# ==============================
# INPUT PARAMETERS
# ==============================

print("binary string size:", sys.argv[1])
print("Number of nodes:", sys.argv[2])
print("Mutation rate:", sys.argv[3])
print("Duration:", sys.argv[4])
print("Infection probability:", sys.argv[5])

sequence_length = int(sys.argv[1])
network_size = int(sys.argv[2])
mutation_rate = float(sys.argv[3])
standard_timer = int(sys.argv[4])
infection_probability = float(sys.argv[5])

total_iterations = 5000
num_runs = 100


# ==============================
# WAXMAN GRAPH
# ==============================

def waxman_graph(n, states, beta=0.3, alpha=0.2, L=None, domain=(0,0,1,1)):
    G = nx.empty_graph(n)

    (xmin, ymin, xmax, ymax) = domain
    pos = {v: (random.uniform(xmin, xmax), random.uniform(ymin, ymax)) for v in G}
    nx.set_node_attributes(G, pos, "pos")

    metric = math.dist

    if L is None:
        L = max(metric(x, y) for x, y in combinations(pos.values(), 2))
        def dist(u, v):
            return metric(pos[u], pos[v])
    else:
        def dist(u, v):
            return random.random() * L

    def should_join(pair):
        return random.random() < beta * math.exp(-dist(*pair) / (alpha * L))

    G.add_edges_from(filter(should_join, combinations(G, 2)))

    # initialize infection status
    status = {v: random.choice(states) for v in G}
    nx.set_node_attributes(G, status, "status")

    # make most inactive
    for node in G:
        if G.nodes[node]["status"] != "":
            if random.random() <= 0.8:
                G.nodes[node]["status"] = ""

    # initialize timers
    timer = {v: random.choice([1,2,3]) for v in G}
    nx.set_node_attributes(G, timer, "timer")

    for node in G:
        if G.nodes[node]["status"] == "":
            G.nodes[node]["timer"] = 0

    return G


# ==============================
# FITNESS LANDSCAPE
# ==============================

def create_hypercube():
    hc = hg.hypercube(2, sequence_length)
    hc.get_all_vertices()
    hc.build_hypercube()
    return hc


def generate_initial_states(H):
    states = [""]
    states.append(H.get_least_fit_state())
    return states


# ==============================
# MUTATION
# ==============================

def Simulated_Annealing(H, state, T, Tmin=0.00001, alpha=0.9):
    neighbors = list(H.get_neighbors(state).keys())
    current_state = state

    while T >= Tmin:
        new_state = random.choice(neighbors)
        delta_E = H.get_fitness(new_state) - H.get_fitness(current_state)

        if delta_E > 0:
            current_state = new_state
        elif random.random() < math.exp(delta_E / T):
            current_state = new_state

        T *= alpha

    return current_state


def Mutation(G, H):
    T_init = 2 ** sequence_length

    for node in G:
        if G.nodes[node]["status"] != "":
            next_state = Simulated_Annealing(H, G.nodes[node]["status"], T_init)
            if random.random() < mutation_rate:
                G.nodes[node]["status"] = next_state


# ==============================
# FIXED INFECTION MODEL
# ==============================

def Infection_Decision(G, H, gamma):
    """
    Infection probability depends on number of infected neighbors:
        P = 1 - (1 - gamma)^m

    If infection occurs, strain is chosen probabilistically
    proportional to (prevalence × fitness).
    """
    infected_list = {}

    for node in G:
        if G.nodes[node]["status"] == "":

            # Identify infected neighbors
            infected_neighbors = [
                n for n in G.neighbors(node)
                if G.nodes[n]["status"] != ""
            ]

            m = len(infected_neighbors)

            if m == 0:
                continue

            # Contact-dependent infection probability
            p_infect = 1 - (1 - gamma) ** m

            if random.random() <= p_infect:

                # Count strains in neighborhood
                strain_count = {}
                for n in infected_neighbors:
                    s = G.nodes[n]["status"]
                    strain_count[s] = strain_count.get(s, 0) + 1

                # Compute weights: prevalence × fitness
                strain_weight = {}
                for s in strain_count:
                    prevalence = strain_count[s] / m
                    fitness = H.get_fitness(s)
                    strain_weight[s] = prevalence * fitness

                # --- OPTION B CHANGE ---
                # Convert weights into probabilities and sample strain

                strains = list(strain_weight.keys())
                weights = np.array([strain_weight[s] for s in strains])

                total_weight = weights.sum()

                if total_weight > 0:
                    probabilities = weights / total_weight
                    chosen_strain = np.random.choice(strains, p=probabilities)
                    infected_list[node] = chosen_strain
                else:
                    # fallback (should rarely happen)
                    chosen_strain = random.choice(strains)
                    infected_list[node] = chosen_strain

    return infected_list


def update_timer_and_status(G):
    for node in G:
        if G.nodes[node]["status"] != "":
            if G.nodes[node]["timer"] < standard_timer:
                G.nodes[node]["timer"] += 1
            else:
                G.nodes[node]["status"] = ""
                G.nodes[node]["timer"] = 0


def Infection_and_Disinfection(G, infection_list):
    update_timer_and_status(G)

    for node in infection_list:
        G.nodes[node]["status"] = infection_list[node]
        G.nodes[node]["timer"] = 1


# ==============================
# MAIN SIMULATION LOOP
# ==============================

def Infection_Propagation(G, H):

    for t in range(total_iterations):

        active_states = [
            G.nodes[n]["status"] for n in G
            if G.nodes[n]["status"] != ""
        ]

        if H.get_fittest_state() in active_states:
            return t

        if len(active_states) == 0:
            return t

        Mutation(G, H)

        infection_list = Infection_Decision(G, H, infection_probability)
        Infection_and_Disinfection(G, infection_list)

    return total_iterations


# ==============================
# RUN MULTIPLE REPLICATES
# ==============================

hypercube = create_hypercube()
states = generate_initial_states(hypercube)

walk_lengths = []

for run in range(num_runs):
    G = waxman_graph(network_size, states, domain=(0,0,10,10))
    walk_length = Infection_Propagation(G, hypercube)

    print(f"Run {run+1}: walk_length = {walk_length}")
    walk_lengths.append(walk_length)

walk_lengths = np.array(walk_lengths)

mean_walk = np.mean(walk_lengths)
std_walk = np.std(walk_lengths)

print("\n==============================")
print("Mean adaptive walk:", mean_walk)
print("Std dev:", std_walk)
print("N:", len(walk_lengths))
print("==============================")
