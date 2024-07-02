import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.creaGrafo()
        self._view.txt_result.controls.append(ft.Text(f"nodi: {self._model.dettagliGrafo()[0]}, archi: {self._model.dettagliGrafo()[1]}"))
        self._view.txt_result.controls.append(ft.Text(f"minimo: {self._model.minMax()[0]}, massimo: {self._model.minMax()[1]}"))
        self._view.update_page()

    def handle_countedges(self, e):
        soglia = int(self._view.txt_name.value)
        if soglia < self._model.minMax()[0] or soglia > self._model.minMax()[1]:
            self._view.create_alert("suca")
        else:
            maggiori, minori = self._model.contaSoglia(soglia)
            self._view.txt_result.controls.append(ft.Text(f"maggiori della soglia: {maggiori}, minori: {minori}"))
        self._view.update_page()

    def handle_search(self, e):
        soglia = int(self._view.txt_name.value)
        sol, costo = self._model.cercaPercorso(soglia)
        self._view.txt_result2.controls.append(ft.Text(f"soluzione: {sol}"))
        self._view.txt_result2.controls.append(ft.Text(f"costo: {costo}"))
        self._view.update_page()
