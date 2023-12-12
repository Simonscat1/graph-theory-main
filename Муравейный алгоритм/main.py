import random

class ant_algorithm:
    def __init__(self, graphLen, graph, num_iterations):
        self.graphLen = graphLen
        self.graph = graph
        self.num_iterations = num_iterations

    def next_sity(self, current_city, visited_cities, pheromone):
        cities = set(c for c, _ in self.graph[current_city]) - set(visited_cities)
        if not cities:
            return random.choice(list(set(self.graph.keys()) - set(visited_cities)))
        probabilities = []
        for city in cities:
            numerator = pheromone[(current_city, city)]
            denominator = 0
            for c in cities:
                denominator += pheromone[(current_city, c)]
            probability = numerator / denominator
            probabilities.append(probability)
        return random.choices(list(cities), probabilities)[0]

    def updatePheromones(self, pheromone, allPaths, decay=0.1):
        for k, v in pheromone.items():
            pheromone[k] = v * (1.0 - decay)
        for path, cost in allPaths:
            for i in range(len(path) - 1):
                if (path[i], path[i + 1]) in pheromone and cost != 0:
                    pheromone[(path[i], path[i + 1])] += 1.0 / cost
        return pheromone

    def pathCost(self, path):
        if(len(path) <2):
            return 0
        cost = 0
        for i in range(1, len(path)):
            found = False
            for city, cost in self.graph[path[i - 1]]:
                if city == path[i]:
                    cost += cost
                    found = True
                    break
            if not found:
                cost += 0
        return cost

    def algorithm(self):
        pheromone = {}
        for city in self.graph:
            for city1, _ in graph[city]:
                pheromone[(city,city1)] = 1
        allPath = []

        for i in range(self.num_iterations):
            for _ in range(self.graphLen):
                path = [random.choice(list(graph.keys()))]
                while len(path) < self.graphLen:
                    sity = self.next_sity(path[-1], path, pheromone)
                    if sity is None:
                        break
                    path.append(sity)
                if(path[-1], path[0]) not in pheromone:
                    continue
                allPath.append((path, self.pathCost(path)))
            pheromone = self.updatePheromones(pheromone, allPath)
        return min(allPath, key=lambda x: x[1])

graph = {
    1: [(2, 10), (3, 6), (4, 8)],
    2: [(4, 5), (7, 11)],
    3: [(5, 3)],
    4: [(3, 2), (5, 5), (6, 7), (7, 12)],
    5: [(6, 9), (9, 12)],
    6: [(8, 8), (9, 10)],
    7: [(6, 4), (8, 6)],
    8: [(9, 1)],
    9: []
}

s = ant_algorithm(len(graph), graph, 1000)
print(s.algorithm())