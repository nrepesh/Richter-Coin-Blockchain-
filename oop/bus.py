from vehicle import Vehicle

class Bus(Vehicle):
    def __init__(self,staring_top_speed = 100):
        super().__init__(staring_top_speed)
        self.passengers = []


bus1 = Bus(50)
bus1.warning.append('Test')
print(bus1.passengers)
bus1.drive()