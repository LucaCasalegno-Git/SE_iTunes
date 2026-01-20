import networkx as nx

from database.dao import DAO



class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.nodes = []
        self.edges = []

        self.lista_album = []
        self.lista_conn_album = []
        self.id_map_album = {}

        self.sol_migliore = []


    def build_graph(self,soglia):
        self.G.clear()
        self.nodes = []
        self.edges = []

        self.lista_album = DAO.read_album(soglia)
        self.lista_conn_album = DAO.read_connesioni_album(soglia)

        self.id_map_album = {}
        for a in self.lista_album:
            self.id_map_album[a.id] = a

        for a in self.lista_album:
            self.nodes.append(a)
        self.G.add_nodes_from(self.nodes)

        for a1, a2 in self.lista_conn_album:
            if a1 in self.id_map_album and a2 in self.id_map_album:
                self.edges.append((self.id_map_album[a1], self.id_map_album[a2]))
        self.G.add_edges_from(self.edges)

    def get_connected_components(self, album):
        con = nx.node_connected_component(self.G, album)
        return con

    def durata_album_parte_connessa(self, connessa):
        durata_totale = 0
        for n in connessa:
            durata_totale += n.durata
        return durata_totale

    def cerca_set_album(self, max_durata_totale, album):
        componente_connessa = self.get_connected_components(album)
        self.sol_migliore = []
        self._ricorsione(componente_connessa,[album], album.durata, max_durata_totale)
        return self.sol_migliore

    def _ricorsione(self,componente_connessa, parziale, durata_parziale, max_durata_totale):

        if len(parziale) > len(self.sol_migliore):
            self.sol_migliore = parziale[:]

        for album in componente_connessa:
            if album in parziale:
                continue
            nuova_durata = durata_parziale + album.durata
            if nuova_durata <= max_durata_totale:
                parziale.append(album)
                self._ricorsione(componente_connessa, parziale, nuova_durata, max_durata_totale)
                parziale.pop()




