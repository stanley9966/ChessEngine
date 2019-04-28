import chess

class State(object):
    def __init__(self): 
        self.board = chess.Board()

    def edges(self):
        self.board.generate_legal_moves

    def values(self):
        return 1    # not sure why returning 1 here

if __name__ == "__main__":
    s = State()
    print(s.edges())
