import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._customers = None
        self._hours = None
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._solBest = []
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, 0)

    def ricorsione(self, parziale, maxY, maxH, pos):
        # TO FILL
        if self.calcola_ore(parziale) > maxH and self.vincolo_anni(parziale, maxY):
            if self.migliorante(parziale, self._customers):
                if len(self._solBest)==0:
                    self._solBest.append(copy.deepcopy(parziale))
                    self._customers = self.calcola_persone(parziale)
                    self._hours = self.calcola_ore(parziale)
                else:
                    self._solBest.pop()
                    self._solBest.append(copy.deepcopy(parziale))
                    self._customers = self.calcola_persone(parziale)
                    self._hours = self.calcola_ore(parziale)
        else:
            for po in self._listEvents[pos:]: #la lista è sempre uguale ma devo escludere i casi già fatti
                parziale.append(po)
                if self.vincolo_anni(parziale, maxY) and self.vincolo_ore(parziale, maxH):
                    self.ricorsione(parziale, maxY, maxH, pos+1)
                parziale.pop()

    def calcola_ore(self, parziale):
        tot_ore = 0
        if len(parziale) == 0:
            return tot_ore
        else:
            for po in parziale:
                tot_ore += (po.date_event_finished - po.date_event_began).total_seconds() #formato date
            hours = divmod(tot_ore, 3600)[0]
            return hours

    def calcola_persone(self, parziale):
        tot_persone = 0
        if len(parziale) == 0:
            return tot_persone
        else:
            for po in parziale:
                tot_persone += po.customers_affected
            return tot_persone

    def migliorante(self, parziale, customers):
        persone = self.calcola_persone(parziale)
        if customers is None:
            return True
        elif persone>customers:
            return True
        else:
            return False

    def vincolo_anni(self, parziale, maxY):
        if len(parziale)==0:
            return True
        anni = parziale[0].date_event_began.year - parziale[-1].date_event_began.year
        if anni < maxY:
            return True
        else:
            return False

    def vincolo_ore(self, parziale, maxH):
        ore = self.calcola_ore(parziale)
        if len(parziale)==0:
            return True
        elif ore<=maxH:
            return True
        else:
            return False

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc