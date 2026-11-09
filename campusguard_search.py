%%writefile campusguard_search.py
import heapq
import itertools
import time
from collections import deque
 
ACCIONES = {
    "a1_notificar": dict(dG=0, dA=0, dE=0, dL=1, costo=1, tope=1),
    "a2_tutoria": dict(dG=1, dA=0, dE=0, dL=0, costo=4, tope=3),
    "a3_bienestar": dict(dG=0, dA=1, dE=0, dL=1, costo=5, tope=3),
    "a4_revision_carga": dict(dG=0, dA=0, dE=-1, dL=0, costo=4, tope=2),
    "a5_seguimiento": dict(dG=0, dA=1, dE=0, dL=1, costo=2, tope=4),
}
 
NOMBRES = list(ACCIONES)
 
UMBRAL_BAJO = 400
 
S0 = (4, 5, 4, 0, 1, 0, 0, 0, 0, 0)
 
def riesgo_milli(s):
    G, A, E, L, H = s[:5]
    return 35*(10-G) + 30*(10-A) + 50*min(E, 4) + 20*max(5-L, 0) + 50*H
 
def delta_max(a):
    return 35*a["dG"] + 30*a["dA"] + 50*max(-a["dE"], 0) + 20*a["dL"]
 
class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
 
    def actions(self, state):
        raise NotImplementedError
 
    def result(self, state, action):
        raise NotImplementedError
 
    def goal_test(self, state):
        return state == self.goal
 
    def path_cost(self, c, s1, a, s2):
        return c + 1
 
    def h(self, node):
        return 0
 
class CampusGuard(Problem):
 
    def actions(self, s):
        return [
            n for i, n in enumerate(NOMBRES)
            if s[5 + i] < ACCIONES[n]["tope"]
        ]
 
    def result(self, s, action):
        i = NOMBRES.index(action)
        a = ACCIONES[action]
 
        G, A, E, L, H = s[:5]
 
        usos = list(s[5:])
        usos[i] += 1
 
        return (
            min(G + a["dG"], 10),
            min(A + a["dA"], 10),
            max(E + a["dE"], 0),
            min(L + a["dL"], 5),
            H,
            *usos
        )
 
    def goal_test(self, s):
        return riesgo_milli(s) < UMBRAL_BAJO
 
    def path_cost(self, c, s1, action, s2):
        return c + ACCIONES[action]["costo"]
 
    def h(self, node):
 
        s = node.state
        falta = max(0, riesgo_milli(s) - (UMBRAL_BAJO - 1))
 
        if falta == 0:
            return 0.0
 
        items = []
 
        for i, n in enumerate(NOMBRES):
            a = ACCIONES[n]
            k = a["tope"] - s[5 + i]
 
            if k > 0:
                items.append(
                    (delta_max(a) / a["costo"],
                     delta_max(a),
                     a["costo"],
                     k)
                )
 
        items.sort(reverse=True)
 
        h = 0.0
 
        for _, d, c, k in items:
 
            if falta <= 0:
                break
 
            u = min(k, falta / d)
            h += u * c
            falta -= u * d
 
        return h if falta <= 1e-9 else float("inf")
 
class Node:
 
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0
 
    def expand(self, problem):
        return [
            self.child_node(problem, a)
            for a in problem.actions(self.state)
        ]
 
    def child_node(self, problem, action):
        nxt = problem.result(self.state, action)
 
        cost = problem.path_cost(
            self.path_cost,
            self.state,
            action,
            nxt
        )
 
        return Node(nxt, self, action, cost)
 
    def solution(self):
        return [n.action for n in self.path()[1:]]
 
    def path(self):
        n = self
        out = []
 
        while n:
            out.append(n)
            n = n.parent
 
        return out[::-1]
 
    def __lt__(self, other):
        return self.state < other.state
