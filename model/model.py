import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.DiGraph()
        self.rifugio_dict = {}
        self.edges_sup = []
        self.edges_inf = []

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        lista_rifugi = DAO.getAllrifugi()
        for r in lista_rifugi:
            self.rifugio_dict[r.id] = r
        lista_connessioni = DAO.getAllconnessioni_for_year(year)
        for c in lista_connessioni:
            self.G.add_edge(self.rifugio_dict[c.id_rifugio1], self.rifugio_dict[c.id_rifugio2], weight=c.weight)
        return self.G

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        weights = []
        for id1, id2, w in self.G.edges(data="weight"):
            weights.append(w)
        min_weight = min(weights)
        max_weight = max(weights)
        return min_weight, max_weight

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        self.edges_sup = []
        for u, v, attrs in self.G.edges(data=True):
            if attrs['weight'] > soglia:
                self.edges_sup.append((u, v))
        self.edges_inf = []
        for u, v, attrs in self.G.edges(data=True):
            if attrs['weight'] < soglia:
                self.edges_inf.append((u, v))
        return len(self.edges_inf), len(self.edges_sup)

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo(self):
        a = self.cammino_minimo_dijkstra()
        b = self.cammino_minimo_ricorsivo()
        return b

    def cammino_minimo_dijkstra(self):
        G_filtrato = self.G.edge_subgraph(self.edges_sup)
        path_minimo = None
        result = []
        for source in G_filtrato.nodes():
            for target in G_filtrato.nodes():
                if source != target:
                    try:
                        path = nx.single_source_dijkstra(G_filtrato, source, target, cutoff = None, weight='weight')
                        if len(path[1]) > 2:
                            if path_minimo is None or path[0] < path_minimo[0] :
                                path_minimo = path
                    except nx.exception.NetworkXNoPath:
                        pass

        if path_minimo is not None:
            for i in range(1,len(path_minimo[1])):
                result.append([path_minimo[1][i-1], path_minimo[1][i],G_filtrato[path_minimo[1][i-1]][path_minimo[1][i]]])
            return result
        else: return []

    def cammino_minimo_ricorsivo(self):
        G_filtrato = self.G.edge_subgraph(self.edges_sup).copy()
        self.best_result = [None, None]
        self.visitati = set()
        self.cammino_corrente = []
        self.peso_corrente = 0
        nodi = list(G_filtrato.nodes())
        for source in nodi:
            for target in nodi:
                if source == target:
                    continue
                self.visitati = {source}
                self.cammino_corrente = [source]
                self.peso_corrente = 0
                best_locale = [None, None]
                self.dfs_minimo(G_filtrato, source, target, best_locale)
                if best_locale[0] is not None:
                    if self.best_result[0] is None or best_locale[0] < self.best_result[0]:
                        self.best_result = best_locale
        if self.best_result[0] is None:
            return []
        nodi_cammino = self.best_result[1]
        risultato = []
        for i in range(1, len(nodi_cammino)):
            u = nodi_cammino[i - 1]
            v = nodi_cammino[i]
            risultato.append([u, v, G_filtrato[u][v]])
        return risultato

    def dfs_minimo(self, G_filtrato, corrente, destinazione, best_locale):
        if best_locale[0] is not None and self.peso_corrente >= best_locale[0]:
            return
        if corrente == destinazione:
            if len(self.cammino_corrente) >= 3:
                best_locale[0] = self.peso_corrente
                best_locale[1] = list(self.cammino_corrente)
            return
        for vicino in G_filtrato.successors(corrente):
            if vicino in self.visitati:
                continue
            peso_arco = G_filtrato[corrente][vicino]['weight']
            self.visitati.add(vicino)
            self.cammino_corrente.append(vicino)
            self.peso_corrente += peso_arco
            self.dfs_minimo(G_filtrato, vicino, destinazione, best_locale)
            self.peso_corrente -= peso_arco
            self.cammino_corrente.pop()
            self.visitati.remove(vicino)