import json
import sys


class SimulatedCommunication:
    def __init__(self, tracker=False):
        self.tracker = tracker
        self.received = list()
        self.sent = list()

    def send(self, data):
        if self.tracker:
            self.sent.append(sys.getsizeof(data))
        return data

    def receive(self, data):
        if self.tracker:
            self.received.append(sys.getsizeof(data))
        return data


class Simulation:
    def __init__(self, server, fragment, subpoint=None, communication=None):
        self.server = server
        self.fragment = fragment
        self.subpoint = list() if subpoint is None else subpoint
        self.communication = SimulatedCommunication() if communication is None else communication

    def __getitem__(self, item):
        return Simulation(self.server, self.fragment, self.subpoint + [item], communication=self.communication)

    def _binoperator(self, name, other):
        method = name
        payload = {
            "subpoint": self.subpoint,
            "kwargs": {"other": [other.fragment]+other.subpoint if isinstance(other, Simulation) else other},
        }
        #print(method, self.fragment, payload)
        payload = self.communication.send(payload)
        response, status_code = self.server.manual_request(self.fragment, method, payload)
        response, status_code = self.communication.receive((response, status_code))
        response = json.loads(response)
        if status_code == 200:
            return str(response)
        else:
            return f"Failed to execute {method}. Status code: {status_code}"

    def operator(self, name, other):
        return Simulation(self.server, self._binoperator(name, other), communication=self.communication)

    def __mul__(self, other):
        return Simulation(self.server, self._binoperator("__mul__", other), communication=self.communication)

    def __add__(self, other):
        return Simulation(self.server, self._binoperator("__add__", other), communication=self.communication)

    def __radd__(self, other):
        return Simulation(self.server, self._binoperator("__radd__", other), communication=self.communication)

    def __sub__(self, other):
        return Simulation(self.server, self._binoperator("__sub__", other), communication=self.communication)

    def __rsub__(self, other):
        return Simulation(self.server, self._binoperator("__rsub__", other), communication=self.communication)

    def __pow__(self, other):
        return Simulation(self.server, self._binoperator("__pow__", other), communication=self.communication)

    def __rpow__(self, other):
        return Simulation(self.server, self._binoperator("__rpow__", other), communication=self.communication)

    def __rmul__(self, other):
        return Simulation(self.server, self._binoperator("__rmul__", other), communication=self.communication)

    def __eq__(self, other):
        return Simulation(self.server, self._binoperator("__eq__", other), communication=self.communication)

    def __ne__(self, other):
        return Simulation(self.server, self._binoperator("__ne__", other), communication=self.communication)

    def __lt__(self, other):
        return Simulation(self.server, self._binoperator("__lt__", other), communication=self.communication)

    def __le__(self, other):
        return Simulation(self.server, self._binoperator("__le__", other), communication=self.communication)

    def __gt__(self, other):
        return Simulation(self.server, self._binoperator("__gt__", other), communication=self.communication)

    def __ge__(self, other):
        return Simulation(self.server, self._binoperator("__ge__", other), communication=self.communication)

    def __abs__(self):
        return Simulation(self.server, self._binoperator("__abs__", ""), communication=self.communication)

    def run(self, request):
        method, kwargs = request
        payload = {"subpoint": self.subpoint, "kwargs": kwargs}
        payload = self.communication.send(payload)
        response, status_code = self.server.manual_request(self.fragment, method, payload)
        response, status_code = self.communication.receive((response, status_code))
        response = json.loads(response)
        if status_code == 200:
            return response
        else:
            return f"Failed to execute {method}. Status code: {status_code}"
