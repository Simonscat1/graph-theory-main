def dijkstra(graph, start_point, end_point):
    short_paths = {start_point: (None, 0)}
    queue = [(0, start_point)]
    while queue:
        queue.sort()
        (distance, current_point) = queue.pop(0)
        for neighbour, weight in graph[current_point].items():
            old_distance = short_paths.get(neighbour, (None, float('inf')))[1]
            new_distance = distance + weight
            if new_distance < old_distance:
                short_paths[neighbour] = (current_point, new_distance)
                queue.append((new_distance, neighbour))
    path = []
    current_point = end_point
    while current_point is not None:
        path.append(current_point)
        next_point = short_paths[current_point][0]
        current_point = next_point
    path = path[::-1]  # Переворачиваем путь, чтобы он начинался от начальной вершины
    return path, short_paths[end_point][1]

graph = {
    '1': {'2': 10, '4': 8, '3': 6},
    '2': {'4': 5, '7': 11},
    '3': {'5': 3},
    '4': {'3': 2, '5': 5, '6': 7, '7': 12},
    '5': {'6': 9, '9': 12},
    '6': {'8': 8, '9': 10},
    '7': {'6': 4, '8': 6},
    '8': {'9': 15},
    '9': {}
}

path, distance = dijkstra(graph, '1', '9')
print('Кратчайший путь: ', ' -> '.join(path))
print('Общее расстояние: ', distance)
