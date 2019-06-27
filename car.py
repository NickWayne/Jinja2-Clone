class car(object):

    def __init__(self):
        self.make = "VW"
        self.model = "Jetta"
        
    def stringify(self, data):
        return "I am a {} {} and it {}".format(self.make, self.model, data)
