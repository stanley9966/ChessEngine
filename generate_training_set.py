import os
import chess.pgn
import numpy as np
from state import State

def get_dataset(num_samples=None):
    X,Y = [], []
    game_number = 0
    values_dict = {"1/2-1/2":0, "0-1":-1, "1-0":1}

    for fn in os.listdir("data"):
        pgn = open(os.path.join("data", fn)) # opening every file data dir
        while 1:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            res = game.headers['Result']
            if res not in values_dict:
                continue
            value = values_dict[res]
            board = game.board()

            for i, move in enumerate(game.mainline_moves()):
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)
                Y.append(value)

            print("parsing game {}, now has {} examples".format(game_number, len(X)))
            game_number += 1

            if num_samples is not None and len(X) > num_samples:
                return X,Y

    X = np.array(X)
    Y = np.array(Y)
    return X,Y

if __name__ == "__main__":
    X,Y = get_dataset(4000000)    # 4 million board states, including same games though
    np.savez("processed_games.npz", X, Y)
