class CMS7Error(Exception):
    def __init__(self, message):
        self.message = message
