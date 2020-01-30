import vehicle

class Car(vehicle.Vehicle):
    # top_speed = 100
    # warning = []
    pass

c = Car()
c.drive()
c.warning.append('new')

Car.top_speed = 200

c2 = Car(200)
c2.drive()
print(c2.warning)