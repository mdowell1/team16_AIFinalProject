import chess
import random
from time import sleep


class HumanPlayer:  # class for human
    def __init__(self):
        self.id = 0  # id may be used or removed later

    @staticmethod
    def move(board):  # make a move and return it to the caller
        legal_moves = list(board.legal_moves)
        move = input("Enter move: ")  # get the move input from the player
        while chess.Move.from_uci(move) not in legal_moves:  # if it isn't in the set of legal moves
            move = input("That is not a valid move; please enter a valid move: ")  # display this and get new input

        return chess.Move.from_uci(move)  # return the move


class AIPlayer:  # class for AI player
    def __init__(self):
        self.id = 0  # id may be used or removed later

    @staticmethod
    def move(board):  # make a move and return it to the caller - currently random for baseline
        legal_moves = list(board.legal_moves)  # get a list of the legal moves
        sleep(1)  # pause so it doesn't happen too quickly - player should see the movement
        return random.choice(legal_moves)  # return a random move from the list of legal moves
