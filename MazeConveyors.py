from collections import deque
def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:

    rows = len(maze)
    cols = len(maze[0])

    start = None
    end = None

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if start is None:
        return {
            "distance": -1,
            "path": []
        }

    if end is None:
        end = start
        
    directions = [
        (-1, 0),  # ขึ้น
        (1, 0),   # ลง
        (0, -1),  # ซ้าย
        (0, 1)    # ขวา
    ]

    conveyor = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    queue = deque([start])

    visited = {start}
    parent = {start: None}
    distance = {start: 0}

    while queue:

        r, c = queue.popleft()

        # ถึง E
        if (r, c) == end:
            break

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue

            if maze[nr][nc] == '#':
                continue

            positions = [(nr, nc)]

            while maze[nr][nc] in conveyor:

                cdr, cdc = conveyor[maze[nr][nc]]

                next_r = nr + cdr
                next_c = nc + cdc

                if (
                    next_r < 0
                    or next_r >= rows
                    or next_c < 0
                    or next_c >= cols
                    or maze[next_r][next_c] == '#'
                ):
                    break

                nr = next_r
                nc = next_c

                positions.append((nr, nc))

            final_pos = (nr, nc)

            if final_pos not in visited:

                visited.add(final_pos)

                previous = (r, c)

                for pos in positions:
                    parent[pos] = previous
                    previous = pos

                distance[final_pos] = distance[(r, c)] + 1

                queue.append(final_pos)

    if end not in visited:
        return {
            "distance": -1,
            "path": []
        }

    path = []
    current = end

    while current is not None:
        path.append([current[0], current[1]])
        current = parent[current]


    path.reverse()

    return {
        "distance": distance[end],
        "path": path
    }

if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}