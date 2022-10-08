import random


class ARIMa:

    def __init__(self, input) -> None:
        self.input = input

    def fit(self):
        return [(i + random.randrange(-10, 100)) * 6 for i in self.input]
