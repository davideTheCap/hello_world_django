class Person(object):

    # Constructor
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

    # Display method inside the class
    def Display(self):
        print(self.name, self.id)
