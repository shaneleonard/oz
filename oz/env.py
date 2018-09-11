import jinja2
import whoosh

class Environment:
    def __init__(self):
        self.callbacks = {}
        self.items = {}

    def register(self, key, callback):
        self.callbacks[key] = callback

    def __getitem__(self, key):
        if key not in self.items:
            self.items[key] = self.callbacks[key]()
        return self.items[key]

env = Environment()
