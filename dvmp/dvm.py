class Dvm:
    def __init__(self):
        self._store = dict()

    def load(self, variable: str):
        if variable not in self._store:
            return None
        return self._store[variable]
    
    def store(self, variable: str, value):
        self._store[variable] = value

    def exists(self, variable: str):
        return variable in self._store
    
