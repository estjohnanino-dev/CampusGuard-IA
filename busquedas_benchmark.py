%%writefile busquedas_benchmark.Py
import heapq
import itertools
import time
from collections import deque
 
from campusguard_search import CampusGuard, Node, S0, riesgo_milli
 
 
def breadth_first_graph_search(problem):
    node = Node(problem.initial)
    n_exp = 0
 
    if problem.goal_test(node.state):
        return node, 0
 
    frontier = deque([node])
    explored = set()
    en_frontera = {node.state}
 
    while frontier:
        node = frontier.popleft()
        en_frontera.discard(node.state)
 
        explored.add(node.state)
        n_exp += 1
 
        for child in node.expand(problem):
 
            if (child.state not in explored and
                    child.state not in en_frontera):
 
                if problem.goal_test(child.state):
                    return child, n_exp
 
                frontier.append(child)
                en_frontera.add(child.state)
 
    return None, n_exp
 
 
def depth_first_graph_search(problem):
 
    frontier = [Node(problem.initial)]
    explored = set()
    n_exp = 0
 
    while frontier:
 
        node = frontier.pop()
 
        if problem.goal_test(node.state):
            return node, n_exp
 
        if node.state in explored:
            continue
 
        explored.add(node.state)
        n_exp += 1
 
        for child in reversed(node.expand(problem)):
            if child.state not in explored:
                frontier.append(child)
 
    return None, n_exp
 
 
def astar_search(problem, h=None):
 
    h = h or problem.h
 
    contador = itertools.count()
    start = Node(problem.initial)
 
    frontier = [(h(start), next(contador), start)]
 
    best = {start.state: 0}
    explored = set()
    n_exp = 0
 
    while frontier:
 
        _, _, node = heapq.heappop(frontier)
 
        if node.state in explored:
            continue
 
        if problem.goal_test(node.state):
            return node, n_exp
 
        explored.add(node.state)
        n_exp += 1
 
        for child in node.expand(problem):
 
            if child.state in explored:
                continue
 
            if child.path_cost < best.get(child.state, float("inf")):
 
                best[child.state] = child.path_cost
 
                heapq.heappush(
                    frontier,
                    (
                        child.path_cost + h(child),
                        next(contador),
                        child
                    )
                )
 
    return None, n_exp
 
 
def uniform_cost_search(problem):
    return astar_search(problem, h=lambda n: 0)
 
 
def medir(fn, problem, reps=100):
 
    tiempos = []
 
    for _ in range(reps):
 
        t0 = time.process_time()
        res = fn(problem)
 
        tiempos.append(
            (time.process_time() - t0) * 1000
        )
 
    tiempos.sort()
 
    return res, tiempos[len(tiempos) // 2]
 
 
if __name__ == "__main__":
 
    p = CampusGuard(S0)
 
    optimo = uniform_cost_search(p)[0].path_cost
 
    print(f"s0 = {S0}")
    print(f"r(s0) = {riesgo_milli(S0)/1000:.3f}")
    print(f"costo optimo = {optimo}")
    print()
 
    print("Algoritmo  Expandidos  ms(CPU)  Costo")
 
    for nombre, fn in [
        ("BFS", breadth_first_graph_search),
        ("DFS", depth_first_graph_search),
        ("A*", astar_search)
    ]:
 
        (nodo, n_exp), ms = medir(fn, p)
 
        print(
            f"{nombre:8} "
            f"{n_exp:10d} "
            f"{ms:8.3f} "
            f"{nodo.path_cost:6d}"
        )
 
        print("Plan:", nodo.solution())
        print()
