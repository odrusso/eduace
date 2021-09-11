class HttpError(Exception):
    def __init__(self, description="", status=200):
        super().__init__(self)
        self.description = description
        self.status = status

    @property
    def json(self):
        return {
            "description": self.description,
            "status": self.status,
        }