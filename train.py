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
            best_network = pickle.load(f)
            print("Loaded best network:", best_network)

        p = neat.Population(config)
        
        best_genome = neat.DefaultGenome(0)
        best_genome.key = 0

        net = neat.nn.FeedForwardNetwork.create(best_genome, config)
        net = best_network

        p.population[0] = best_genome
        p.population[0].fitness = 0
        
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
