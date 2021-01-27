class Add:
    def __init__(self, value):
        self.value = value

    def __call__(self, x):
        return x + self.value
