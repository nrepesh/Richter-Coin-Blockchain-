class Vehicle:
    def __init__(self, top = 100):
        self.top_speed = top
        self.warning = []

    def drive(self):
        print('I cant drive faster than {}'.format(self.top_speed))