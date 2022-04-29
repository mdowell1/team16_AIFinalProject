import chess
import random
from time import sleep
import BoardUtils


class HumanPlayer:  # class for human
    def __init__(self):
        # explain how to play
        print("To move, enter the from and to square. If pawn is being promoted, indicate piece to promote to. Example: \n"
              "'d2d4' moves white pawn from d2 to d4.\n"
              "if white pawn is in row 7 in column d, and the player wants to promote it to a queen, 'd7d8q' will make that move.\n"
              "Pieces to promote to: b = bishop, n = knight, r = rook, q = queen")

    @staticmethod
    def move(board):  # make a move and return it to the caller
        legal_moves = list(board.legal_moves)  # get the legal moves
        move = input("Enter move: ")  # get the move input from the player

        while True:  # loop until we get a valid input
            try:
                finalMove = chess.Move.from_uci(move)  # get the uci move
                if finalMove not in legal_moves:  # if it isn't in the set of legal moves
                    move = input("That is not a valid move; please enter a valid move: ")  # display to user
                else:  # if we don't have an exception and the move is in legal moves, break out of loop
                    break
            except:  # if we have an exception, display to user
                move = input("That is not a valid move; please enter a valid move: ")

        return chess.Move.from_uci(move)  # return the move


class AIPlayer:  # class for AI player
    def __init__(self, dif):
        self.moveType = "miniMax"  # type for debugging
        self.difficulty = dif  # get the AI difficulty

    def move(self, board: chess.Board):  # make a move and return it to the caller
        print(board)

        # get random move if AI moveType is random
        if self.moveType == "random":
            return self.randomMove(board)

        # otherwise, get minimax move
        elif self.moveType == "miniMax":
            return self.minimaxMove(board)

    @staticmethod
    def randomMove(board):
        legal_moves = list(board.legal_moves)  # get a list of the legal moves
        sleep(1)  # pause so it doesn't happen too quickly - player should see the movement
        return random.choice(legal_moves)  # return a random move from the list of legal moves

    def minimaxMove(self, board):
        # if easy AI, use depth 2
        if self.difficulty == "beginner":
            move = BoardUtils.GetMove(board, 2)
        # if intermediate AI, use depth 4
        elif self.difficulty == "intermediate":
            move = BoardUtils.GetMove(board, 4)
        # if hard AI, use depth 6
        else:
            move = BoardUtils.GetMove(board, 6)

        return move  # return the move to make
