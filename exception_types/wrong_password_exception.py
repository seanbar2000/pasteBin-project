class WrongPasswordException(Exception):
    def __init__(self):
        super().__init__("Wrong password!")
