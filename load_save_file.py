import os
import pickle

def save_game(player, save_file_number):
    save_file = open(os.path.join('Resources','Save Data','save file' + str(save_file_number)), 'w')
    pickle.dump(player,save_file)
    save_file.close()
