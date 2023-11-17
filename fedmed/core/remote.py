import requests


class Remote:
    def __init__(self, ip, fragment, subpoint=None):
        self.ip = ip
        self.fragment = fragment
        self.subpoint = list() if subpoint is None else subpoint

    def __getitem__(self, item):
        return Remote(self.ip, self.fragment, self.subpoint + [item])

    def _binoperator(self, name, other):
        method = name
        payload = {
            "subpoint": self.subpoint,
            "kwargs": {"other": other.subpoint if isinstance(other, Remote) else other},
        }
        response = requests.post(f"{self.ip}/{self.fragment}/{method}", json=payload)
        if response.status_code == 200:
            return str(response.json())
        else:
            return f"Failed to execute {method}. Status code: {response.status_code}"

    def operator(self, name, other):
        return Remote(self.ip, self._binoperator(name, other))

    def __mul__(self, other):
        return Remote(self.ip, self._binoperator("__mul__", other))

    def __add__(self, other):
        return Remote(self.ip, self._binoperator("__add__", other))

    def __radd__(self, other):
        return Remote(self.ip, self._binoperator("__radd__", other))

    def __sub__(self, other):
        return Remote(self.ip, self._binoperator("__sub__", other))

    def __rsub__(self, other):
        return Remote(self.ip, self._binoperator("__rsub__", other))

    def __pow__(self, other):
        return Remote(self.ip, self._binoperator("__pow__", other))

    def __rpow__(self, other):
        return Remote(self.ip, self._binoperator("__rpow__", other))

    def __rmul__(self, other):
        return Remote(self.ip, self._binoperator("__rmul__", other))

    def __eq__(self, other):
        return Remote(self.ip, self._binoperator("__eq__", other))

    def __ne__(self, other):
        return Remote(self.ip, self._binoperator("__ne__", other))

    def __lt__(self, other):
        return Remote(self.ip, self._binoperator("__lt__", other))

    def __le__(self, other):
        return Remote(self.ip, self._binoperator("__le__", other))

    def __gt__(self, other):
        return Remote(self.ip, self._binoperator("__gt__", other))

    def __ge__(self, other):
        return Remote(self.ip, self._binoperator("__ge__", other))

    def __abs__(self):
        return Remote(self.ip, self._binoperator("__abs__", ""))

    def run(self, request):
        method, kwargs = request
        payload = {"subpoint": self.subpoint, "kwargs": kwargs}
        response = requests.post(f"{self.ip}/{self.fragment}/{method}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to execute {method}. Status code: {response.status_code}"
