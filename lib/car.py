from .constants import *

class Car:
    def __init__(self, image, lane, y_pos):
        self.image = image
        self.rect = image.get_rect(center=(lane, y_pos))
        self.lane = lane
        self.speed = AI_INITIAL_SPEED
    
    def move(self):
        self.rect.y += self.speed
    
    def draw(self):
        screen.blit(self.image, self.rect.topleft)
    
    def detect_collision(self, other_car):
        self_hitbox = self.rect.inflate(-self.rect.width * (1 - HITBOX_SHRINK_FACTOR), 
                                       -self.rect.height * (1 - HITBOX_SHRINK_FACTOR))
        other_hitbox = other_car.rect.inflate(-other_car.rect.width * (1 - HITBOX_SHRINK_FACTOR),
                                              -other_car.rect.height * (1 - HITBOX_SHRINK_FACTOR))
        return self_hitbox.colliderect(other_hitbox)
