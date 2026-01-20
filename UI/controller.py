import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model



    def handle_crea_grafo(self, e,):
        """ Handler per gestire creazione del grafo """""

        try:
            soglia = float(self._view.txt_durata.value)
            self._model.build_graph(soglia)

            #popola dropdown
            self._view.dd_album.value = None
            self._view.dd_album.options.clear()
            for r in self._model.lista_album:
                option = ft.dropdown.Option(key=str(r.id), text=r.title)
                self._view.dd_album.options.append(option)

            self._view.lista_visualizzazione_1.controls.clear()
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Grafo creato: {len(self._model.nodes)} album, {len(self._model.edges)} archi")
            )
        except ValueError:
            self._view.show_alert("Inserire un valore numerico")
            return


        self._view.update()


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        album_id = self._view.dd_album.value
        if album_id is None:
            return None
        return self._model.id_map_album.get(int(album_id))

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        album = self.get_selected_album(e)
        if album is None:
            self._view.show_alert("Seleziona un album.")
            return
        parte_connessa = self._model.get_connected_components(album)
        durata_parte_connessa = self._model.durata_album_parte_connessa(parte_connessa)

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Dimensione componente: {len(parte_connessa)}" )
        )
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Durata totale: {durata_parte_connessa:.2f} minuti "))

        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        try:
            dTOT = float(self._view.txt_durata_totale.value)
        except ValueError:
            self._view.show_alert("Inserire un valore numerico")
            return

        album = self.get_selected_album(e)
        if album is None:
            self._view.show_alert("Seleziona un album.")
            return
        soluzione_migliore = self._model.cerca_set_album(dTOT, album)
        durata_totale = sum(a.durata for a in soluzione_migliore)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f"Set trovato ({len(soluzione_migliore)} album, {durata_totale} minuti):"))

        for album in soluzione_migliore:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"-{album.title} ({album.durata})"))

        self._view.update()