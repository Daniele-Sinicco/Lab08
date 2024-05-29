import copy

import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        self._view._txtOut.clean()
        self._model.worstCase(self._view._ddNerc.value, int(self._view._txtYears.value), int(self._view._txtHours.value))
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected : {self._model._customers}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage : {self._model._hours}"))
        soluzione = copy.deepcopy(self._model._solBest[0])
        for i in soluzione:
            self._view._txtOut.controls.append(ft.Text(i))
        self._view.update_page()
        pass

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
