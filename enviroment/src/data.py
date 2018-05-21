from random import randint

class Data():
    def __init__(self):
        self.context_options = ["rectangle", "paddock", "pond", "playground", "pool", "park"]

    def choose(self, full_list):
        num = randint(0, len(full_list) - 1)
        return full_list[num]