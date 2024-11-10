from .car import *
from .constants import *
class PlayerCar(Car):
    def __init__(self, image, lanes, start_lane):
        super().__init__(image, lanes[start_lane], HEIGHT - 100)
        self.lanes = lanes
        self.current_lane_index = start_lane
    
    def move_left(self):
        if self.current_lane_index > 0:
            self.current_lane_index -= 1
            self.rect.centerx = self.lanes[self.current_lane_index]
    
    def move_right(self):
        if self.current_lane_index < len(self.lanes) - 1:
            self.current_lane_index += 1
            self.rect.centerx = self.lanes[self.current_lane_index]
