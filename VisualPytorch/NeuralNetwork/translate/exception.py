class ModelError(Exception):
    def __init__(self, erro_info):
        super().__init__(self)
        self.error_info = erro_info

    def __str__(self):
        return self.erro_info


