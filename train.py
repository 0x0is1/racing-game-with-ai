from lib.game import Game
import neat
import os
import pickle

NUM_GENERATIONS = 1000

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    if os.path.exists("best_model.pkl"):
        with open("best_model.pkl", "rb") as f:
            best_genome = pickle.load(f)
            print("Loaded best network:", best_genome)

        p = neat.Population(config)
        
        p.population[best_genome.key] = best_genome
        
        print("Continuing training from saved model.")
    else:
        p = neat.Population(config)
        print("No saved model found. Starting training from scratch.")

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    game = Game()
    winner = p.run(game.run, NUM_GENERATIONS)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat")
    run(config_file=config_path)
