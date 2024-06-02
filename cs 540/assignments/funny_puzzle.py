import heapq

def get_manhattan_distance(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            goal_index = goal_state.index(tile)
            distance += abs(i % 3 - goal_index % 3) + abs(i // 3 - goal_index // 3)
    return distance

def get_succ(state):
    empty_indexes = [i for i, x in enumerate(state) if x == 0]
    succ_states = []

    for empty_index in empty_indexes:
        x, y = empty_index % 3, empty_index // 3
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < 3 and 0 <= ny < 3]

        for nx, ny in valid_neighbors:
            neighbor_index = ny * 3 + nx
            new_state = state.copy()
            new_state[empty_index], new_state[neighbor_index] = new_state[neighbor_index], new_state[empty_index]
            succ_states.append(new_state)

    return sorted(succ_states)

def print_succ(state):
    succ_states = get_succ(state)
    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))
def solve(initial_state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    Implement the A* algorithm.
    INPUT:
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along with h values,
        the number of moves, and max queue number in the specified format.
    """

    pq = []  # Priority queue
    heapq.heappush(pq, (
        get_manhattan_distance(initial_state), initial_state, (0, get_manhattan_distance(initial_state), -1)))
    current = heapq.heappop(pq) # current state
    set = []
    closed = []
    maxLen = 0

    while current[1] != goal_state:
        set.append(current[1])
        closed.append(current)
        succStates = get_succ(current[1])
        moves = current[2][0]

        for state in succStates:
            if state not in set:
                dist = get_manhattan_distance(state, goal_state)
                cost = moves + 1 + dist

                heapq.heappush(pq, (cost, state, (moves + 1, dist, len(set) - 1)))
        if maxLen < len(pq):
            maxLen = len(pq)
        current = heapq.heappop(pq)
    correctPath = []
    current_index = current[2][2]

    for i in range(current[2][0]):
        correctPath.insert(0, closed[current_index][2][2])
        current_index = closed[current_index][2][2]
    for i in range(1, len(correctPath)):
        print(
            str(set[correctPath[i]]) + " h=" + str(closed[correctPath[i]][2][1]) + " moves: " + str(closed[correctPath[i]][2][0])
        )
    if len(correctPath) > 0:
        # print_state_info(closed_set[current[2][2]], closed_set_full[current[2][2]][2][1],closed_set_full[current[
        # 2][2]][2][0])
        print(str(set[current[2][2]]) + " h=" + str(closed[current[2][2]][2][1]) + " moves: " +
        str(closed[current[2][2]][2][0]))
    print(str(current[1]) + " h=" + str(current[2][1]) + " moves: " + str(current[2][0]))
    print("Max queue length: "+str(maxLen))

if __name__ == "__main__":
    print_succ([2,5,1,4,0,6,7,0,3])
    print()
    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3]))
    print()
    solve([2,5,1,4,0,6,7,0,3])