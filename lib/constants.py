import pygame

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
ROAD_COLOR = (50, 50, 50)
LANE_COLOR = (255, 255, 0)
BORDER_COLOR = (255, 0, 0)

PLAYER_SPEED = 10
SPAWN_RATE = 30
AI_INITIAL_SPEED = 10
SPEED_INCREMENT = 0.5
LANE_WIDTH = WIDTH // 2
LANES = [WIDTH // 3, 2 * WIDTH // 3]
HITBOX_SHRINK_FACTOR = 1
BORDER_PADDING = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Racing Game")

ai_car_img = pygame.image.load('ai_car.png')
player_car_img = pygame.image.load('player_car.png')
player_car_img = pygame.transform.scale(player_car_img, (50, 90))
ai_car_img = pygame.transform.scale(ai_car_img, (50, 90))
