import chess
import numpy as np

class State(object):
    def __init__(self, board=None): 
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board

    def serialize(self):
        # Initialize the board state
        bstate = np.zeros(64, np.uint8) # there are 64 squares on a board

        # Insert Pieces into board state
        for i in range(64):
            piece = self.board.piece_at(i) # type chess.Piece
            if piece is not None:
                bstate[i] = {"P":1, "N":2, "B":3, "R":4, "Q":5, "K":6, \
                             "p":9, "n":10, "b":11, "r":12, "q":13, "k":14}[piece.symbol()]
        
        # Castling 
        # queen - left, king - right
        if self.board.has_queenside_castling_rights(chess.WHITE):
            assert bstate[0] == 4   # check value of bottom left is a rook
            bstate[0] = 7           # 7 means that this rook is able to castle white
        if self.board.has_kingside_castling_rights(chess.WHITE):
            assert bstate[7] == 4   # check value of bottom right is a rook
            bstate[7] = 7
        if self.board.has_queenside_castling_rights(chess.BLACK):
            assert bstate[56] == 8+4  # checking that is a rook
            bstate[56] = 8+7        # 15 means that black rook is castleable 
        if self.board.has_kingside_castling_rights(chess.BLACK):
            assert bstate[63] == 8+4
            bstate[63] = 8+7 

        # En passant
        if self.board.ep_square is not None:
            assert bstate[self.board.ep_square] == 0 # assert en passant is a pawn
            bstate[self.board.ep_square] = 8
        
        # Reshape into understandable 2D array
        bstate = bstate.reshape(8,8)

        #binary state
        state = np.zeros((5,8,8), np.uint8)

        # 0-3 columns to binary
        # because 14 symbols, which is less than 2^4, that's why shift by 3
        state[0] = (bstate>>3)&1
        state[1] = (bstate>>2)&1
        state[2] = (bstate>>1)&1
        state[3] = (bstate>>0)&1
        state[4] = (self.board.turn*1.0) # 4th is who's turn it is
        
        # 257 bits - 64x4 + 1 - 1 extra bit to reprsent who's turn it is
        return state

    def edges(self):
        return list(self.board.legal_moves)

if __name__ == "__main__":
    s = State()
