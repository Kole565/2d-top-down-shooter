class Specks(list):

    def __init__(self, cfg):
        self.specks = cfg

    def __getitem__(self, i):
        return self.specks[i]

    def get(self):
        return list(self.specks.values())

    def add(self, name, inc):
        self.specks[name] += inc

    def multiply(self, name, mult):
        self.specks[name] *= mult
