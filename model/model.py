import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.cromosomi = DAO.getNodi()
        self.grafo = nx.DiGraph()

    def creaGrafo(self):
        self.grafo.add_nodes_from(self.cromosomi.keys())
        for u in self.grafo.nodes:
            for v in self.grafo.nodes:
                if u != v:
                    if DAO.getArco(u, v):
                        self.grafo.add_edge(u, v, weight=DAO.getArco(u, v))

    def dettagliGrafo(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def minMax(self):
        min = 10
        max = 0
        for edge in self.grafo.edges:
            peso = self.grafo[edge[0]][edge[1]]["weight"]
            if peso > max:
                max = peso
            if peso < min:
                min = peso
        return min, max

    def contaSoglia(self, s):
        maggiori = 0
        minori = 0
        for edge in self.grafo.edges:
            peso = self.grafo[edge[0]][edge[1]]["weight"]
            if peso > s:
                maggiori+=1
            if peso < s:
                minori += 1
        return maggiori, minori

    def cercaPercorso(self, soglia):
        self.soluzioneBest = []
        self.costoBest = 0
        for nodo in self.grafo.nodes:
            self.ricorsione([nodo], soglia)
        return self.soluzioneBest, self.costoBest

    def ricorsione(self, parziale, s):
        vicini = self.nodiVisitabili(parziale, s)
        if len(vicini) == 0:
            if self.calcolaCosto(parziale):
                print("best")
                self.soluzioneBest = copy.deepcopy(parziale)
        else:
            for nodo in vicini:
                parziale.append(nodo)
                self.ricorsione(parziale, s)
                parziale.pop()

    def nodiVisitabili(self, parziale, s):
        ris = []
        for nodo in list(self.grafo.successors(parziale[-1])):
            if self.grafo[parziale[-1]][nodo]["weight"] > s:
                if (parziale[-1], nodo) not in parziale:
                    ris.append(nodo)
        print(list(self.grafo.successors(parziale[-1])))
        print(ris)
        return ris

    def calcolaCosto(self, parziale):
        costo = 0
        for i in range(len(parziale)-1):
            costo += self.grafo[parziale[i]][parziale[i+1]]["weight"]
        if costo > self.costoBest:
            self.costoBest = costo
            return True
        return False