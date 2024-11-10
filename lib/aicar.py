from .car import *

class AI_Car(Car):
    def __init__(self, image, lane):
        super().__init__(image, lane, -90)
        self.speed = AI_INITIAL_SPEED
