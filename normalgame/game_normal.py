import pygame
import random
import sys

# Initialize Pygame and constants
pygame.init()
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
ROAD_COLOR = (50, 50, 50)
LANE_COLOR = (255, 255, 0)
BORDER_COLOR = (255, 0, 0)

PLAYER_SPEED = 10
SPAWN_RATE = 30
AI_INITIAL_SPEED = 4
SPEED_INCREMENT = 0.5
LANE_WIDTH = WIDTH // 2
LANES = [WIDTH // 3, 2 * WIDTH // 3]
HITBOX_SHRINK_FACTOR = 1
BORDER_PADDING = 4

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Lane Traffic Racing Game")

# Load car images
player_car = pygame.image.load('player_car.png')
ai_car = pygame.image.load('ai_car.png')
player_car = pygame.transform.scale(player_car, (50, 90))
ai_car = pygame.transform.scale(ai_car, (50, 90))

# Initialize player and AI car positions
player_rect = player_car.get_rect(center=(LANES[0], HEIGHT - 100))
ai_cars = []
score = 0
clock = pygame.time.Clock()
ai_speed = AI_INITIAL_SPEED
current_lane_index = 0  # Start in the first lane

def spawn_ai_car():
    lane = random.choice(LANES)
    rect = ai_car.get_rect(center=(lane, -90))
    ai_cars.append({"rect": rect, "lane": lane})

def move_ai_cars():
    global score, ai_speed
    for car in ai_cars:
        car["rect"].y += ai_speed
        if car["rect"].y > HEIGHT:
            ai_cars.remove(car)
            score += 1
            if score % 10 == 0:
                ai_speed += SPEED_INCREMENT

def detect_collisions():
    # Shrink player hitbox
    player_hitbox = player_rect.inflate(-player_rect.width * (1 - HITBOX_SHRINK_FACTOR), 
                                        -player_rect.height * (1 - HITBOX_SHRINK_FACTOR))
    for car in ai_cars:
        # If the car is rotated, adjust its hitbox accordingly
        car_hitbox = car["rect"].inflate(-car["rect"].width * (1 - HITBOX_SHRINK_FACTOR), 
                                         -car["rect"].height * (1 - HITBOX_SHRINK_FACTOR))
        
        if car["lane"] == LANES[1]:  # Right lane, rotated AI car
            rotated_car = pygame.transform.rotate(ai_car, 180)
            rotated_rect = rotated_car.get_rect(center=car["rect"].center)
            rotated_hitbox = rotated_rect.inflate(-rotated_rect.width * (1 - HITBOX_SHRINK_FACTOR),
                                                  -rotated_rect.height * (1 - HITBOX_SHRINK_FACTOR))
            if player_hitbox.colliderect(rotated_hitbox):
                return True
        else:
            if player_hitbox.colliderect(car_hitbox):
                return True
    return False

def draw_game():
    screen.fill(GRAY)

    # Draw road
    pygame.draw.rect(screen, ROAD_COLOR, (LANE_WIDTH, 0, LANE_WIDTH * 2, HEIGHT))

    # Draw lane divider
    pygame.draw.line(screen, LANE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Draw player and AI cars with borders
    screen.blit(player_car, player_rect.topleft)
    
    for car in ai_cars:
        if car["lane"] == LANES[1]:
            rotated_car = pygame.transform.rotate(ai_car, 180)
            rotated_rect = rotated_car.get_rect(center=car["rect"].center)
            screen.blit(rotated_car, rotated_rect.topleft)
        else:
            screen.blit(ai_car, car["rect"].topleft)

    # Draw score and speed
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    speed_text = font.render(f"Speed: {ai_speed:.1f}", True, WHITE)
    screen.blit(speed_text, (10, 50))

def display_game_over():
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def reset_game():
    global player_rect, ai_cars, score, ai_speed
    player_rect = player_car.get_rect(center=(LANES[0], HEIGHT - 100))
    ai_cars = []
    score = 0
    ai_speed = AI_INITIAL_SPEED

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if detect_collisions():
        display_game_over()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        reset_game()
                        waiting_for_input = False
                    break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and current_lane_index > 0:
        current_lane_index -= 1
        player_rect.centerx = LANES[current_lane_index]
    if keys[pygame.K_RIGHT] and current_lane_index < len(LANES) - 1:
        current_lane_index += 1
        player_rect.centerx = LANES[current_lane_index]

    # Spawn AI cars in one of the lanes if there is enough space
    if random.randint(1, 100) < SPAWN_RATE:
        if len(ai_cars) == 0 or ai_cars[-1]["rect"].y > HEIGHT // 3:
            spawn_ai_car()

    move_ai_cars()

    draw_game()
    pygame.display.flip()
    clock.tick(60)
