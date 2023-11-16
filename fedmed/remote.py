import requests


class Remote:
    def __init__(self, ip, fragment, subpoint=None):
        self.ip = ip
        self.fragment = fragment
        self.subpoint = list() if subpoint is None else subpoint

    def __getitem__(self, item):
        return Remote(self.ip, self.fragment, self.subpoint + [item])

    # def __mul__(self, other):
    # data = other.data if isinstance(other, Remote) else other
    # return Remote(self.data * data, self.config)

    def run(self, request):
        method, kwargs = request
        payload = {"subpoint": self.subpoint, "kwargs": kwargs}
        response = requests.post(f"{self.ip}/{self.fragment}/{method}", json=payload)
        if response.status_code == 200:
            return str(response.json())
        else:
            return f"Failed to execute {method}. Status code: {response.status_code}"
