class Files:
    def __init__(self):
        self.variable = None

    def get_file(self, prompt):
        self.variable = input(prompt)
        return self.variable
