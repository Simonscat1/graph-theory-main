import random

class ant_algorithm:
    def select_next_city(self, graph, current_city, visited_cities, pheromone):
        cities = set(c for c, _ in graph[current_city])
        probabilities = []
        for city in cities:
            numerator = pheromone[(current_city, city)]
            denominator = 0
            for c in cities:
                denominator += pheromone[(current_city, c)]
            probability = numerator / denominator
            probabilities.append(probability)
        return random.choices(list(cities), probabilities)[0]



    def update_pheromones(self, pheromone, all_paths, decay=0.1):
        for k, v in pheromone.items():
            pheromone[k] = v * (1.0 - decay)
        for path, cost in all_paths:
            for i in range(len(path) - 1):
                if (path[i], path[i + 1]) in pheromone and cost != 0:
                    pheromone[(path[i], path[i + 1])] += 1.0 / cost
        return pheromone


    def path_cost(self, path):
        if len(path) < 2:
            return 0
        total_cost = 0
        for i in range(1, len(path)):
            cost_found = False
            for city, cost in graph[path[i - 1]]:
                if city == path[i]:
                    total_cost += cost
                    cost_found = True
                    break
            if not cost_found:
                total_cost += 0
        return total_cost

    def algorithm(self, graph, num_ants, num_iterations):
        pheromone = {}
        alpha_ants = 0
        max_pheromone = 0
        for city1 in graph:
            for city2, _ in graph[city1]:
                pheromone[(city1, city2)] = 1
        best_path = None
        all_paths = []

        for _ in range(num_iterations):
            for _ in range(num_ants):
                path = [random.choice(list(graph.keys()))]
                total_pheromone = 0
                while len(path) < len(graph):
                    next_city = self.select_next_city(graph, path[-1], path, pheromone)
                    if next_city is None:
                        break
                    path.append(next_city)
                    total_pheromone += pheromone[(path[-2], path[-1])]
                if (path[-1], path[0]) not in pheromone:
                    continue
                all_paths.append((path, self.path_cost(path)))
                if total_pheromone > max_pheromone:
                    max_pheromone = total_pheromone
                    alpha_ants += 1
            pheromone = self.update_pheromones(pheromone, all_paths)

        print(f"Количество альфа-муравьев: {alpha_ants}")
        return min(all_paths, key=lambda x: x[1])



graph = {
    1: [(2, 10), (3, 6), (4, 8)],
    2: [(4, 5), (7, 11), (1, 3)],
    3: [(5, 3), (1, 4)],
    4: [(3, 2), (5, 5), (6, 7), (7, 12), (1, 2)],
    5: [(6, 9), (9, 12), (1, 1)],
    6: [(8, 8), (9, 10), (1, 6)],
    7: [(6, 4), (8, 6), (1, 7)],
    8: [(9, 1), (1, 8)],
    9: [(1, 9)]
}
s = ant_algorithm()
print(s.algorithm(graph, len(graph), 1000))

