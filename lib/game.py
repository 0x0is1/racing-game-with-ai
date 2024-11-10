import pygame
import random
import sys
import neat
import os
import pickle
from .constants import *
from .playercar import *
from .aicar import *
from .visualize import *

pygame.init()

class Game:
    def __init__(self):
        self.player_cars = []
        self.ai_cars = []
        self.score = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.ai_speed = AI_INITIAL_SPEED
        self.spawn_rate = SPAWN_RATE
        self.ge = []
        self.nets = []
        self.generation = 0
        self.highscore = 0

    def spawn_ai_car(self):
        lane = random.choice(LANES)
        ai_car = AI_Car(ai_car_img, lane)
        self.ai_cars.append(ai_car)

    def move_ai_cars(self):
        global AI_INITIAL_SPEED
        for ai_car in self.ai_cars:
            ai_car.move()
            if ai_car.rect.y > HEIGHT:
                self.ai_cars.remove(ai_car)
                self.score += 1
                if(self.score > self.highscore):
                    self.highscore = self.score
                    with open("best_model.pkl", "wb") as f:
                        pickle.dump(self.nets[0], f)
                    print("Model saved.")
                for genome in self.ge:
                    genome.fitness += 5
                if self.score % 10 == 0:
                    self.ai_speed += SPEED_INCREMENT

    def detect_collisions(self):
        for ai_car in self.ai_cars:
            for player_car in self.player_cars:
                if player_car.detect_collision(ai_car):
                    self.nets.pop(self.player_cars.index(player_car))
                    self.ge.pop(self.player_cars.index(player_car))
                    self.player_cars.pop(self.player_cars.index(player_car))

    def draw_game(self):
        screen.fill(GRAY)
        pygame.draw.rect(screen, ROAD_COLOR, (LANE_WIDTH, 0, LANE_WIDTH * 2, HEIGHT))
        pygame.draw.line(screen, LANE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
        for player_car in self.player_cars:
            player_car.draw()
        for ai_car in self.ai_cars:
            ai_car.draw()

        generation_text = self.font.render(f"Generation: {self.generation}", True, WHITE)
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, WHITE)
        alive_text = self.font.render(f"Cars Alive: {len(self.player_cars)}", True, WHITE)
        screen.blit(generation_text, (10, 10))
        screen.blit(highscore_text, (10, 50))
        screen.blit(alive_text, (10, 90))


    def get_sensors(self, player_car):
        closest_in_lane_distance = min(
            [abs(ai_car.rect.y - player_car.rect.y) for ai_car in self.ai_cars if ai_car.rect.x == player_car.rect.x],
            default=999
        )
        closest_left_lane_distance = min(
            [abs(ai_car.rect.y - player_car.rect.y) for ai_car in self.ai_cars if ai_car.rect.x == player_car.rect.x - LANE_WIDTH],
            default=999
        )
        closest_right_lane_distance = min(
            [abs(ai_car.rect.y - player_car.rect.y) for ai_car in self.ai_cars if ai_car.rect.x == player_car.rect.x + LANE_WIDTH],
            default=999
        )
        return (closest_in_lane_distance, closest_left_lane_distance, closest_right_lane_distance, player_car.rect.x)

    def run(self, genomes, config):
        self.generation += 1
        self.score = 0
        run = True

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.player_cars.append(PlayerCar(player_car_img, LANES, 0))
            self.ge.append(genome)

        while run and len(self.player_cars) > 0:
            self.detect_collisions()
            for index, player_car in enumerate(self.player_cars):
                self.ge[index].fitness += 0.1
                sensors = self.get_sensors(player_car)
                output = self.nets[self.player_cars.index(player_car)].activate(sensors)
                move_left, move_right = output
                if move_left > move_right:
                    player_car.move_left()
                elif move_right > move_left:
                    player_car.move_right()
            if random.randint(1, 100) < self.spawn_rate:
                if len(self.ai_cars) == 0 or self.ai_cars[-1].rect.y > HEIGHT // 3:
                    self.spawn_ai_car()
            self.move_ai_cars()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(60)
        draw_net(config, genome)

