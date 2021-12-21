class Question:
    def __init__(self, seed, independent_var):
        self.description = ""
        self.question = ""
        self.seed = seed
        self.independent_var = independent_var

    @property
    def json(self):
        return {
            "description": self.description,
            "question": self.question,
            "independent_var": self.independent_var,
        }
