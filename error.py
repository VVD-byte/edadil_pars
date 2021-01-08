class Status_code_error(Exception):
    def __init__(self, text):
        self.txt = text