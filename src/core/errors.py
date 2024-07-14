class NotFoundInSource(Exception):  # noqa: N818 - Semyon, please fix this
    def __init__(self, info):
        self.info = info
        super().__init__(info)
