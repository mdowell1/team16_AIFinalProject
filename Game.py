import sys
import time
from datetime import timedelta

import chess
import chess.svg
from PyQt5 import QtSvg
from PyQt5.QtCore import QTimer, QByteArray
from PyQt5.QtWidgets import QApplication

import BoardUtils
from Players import AIPlayer, HumanPlayer


class Game:
    def __init__(self, board, players):  # initialize game using a board and players
        self.board = board
        self.players = players
        self.flipped = False  # do not flip the board to begin with

        # if p1 (white) is an AI and p2 (black) is a human, flip the board for the player
        if isinstance(self.players[0], AIPlayer) and isinstance(self.players[1], HumanPlayer):
            self.flipped = True

    # calls move on the players to progress the game
    def performMove(self):
        player = self.players[1 - int(self.board.turn)]  # get the player who needs to make the next move
        move = player.move(self.board)  # get a movement from the player
        self.board.push(move)  # make the move
        print(self.board)
        print()

    # determines if game is over and returns outcome
    def isEnd(self):
        outcome = self.board.outcome()  # get if there is an outcome
        if outcome is None:  # if not, game isn't over
            return None
        print("Hits: {0}, Misses: {1}".format(BoardUtils.hit, BoardUtils.miss))
        return outcome.winner, outcome.termination  # if so, game is over, return the winner and how they won


# class to control the GUI
# GUI Information found here: https://www.cs.dartmouth.edu/~devin/cs76/03_chess/chess.html
class GUI:
    def __init__(self, game):  # initialize with a gui timer, game, app, and widget
        self.timer = None  # a timer is needed so the game doesn't end after the first move
        self.game = game
        self.app = QApplication(sys.argv)  # create an application
        self.widget = QtSvg.QSvgWidget()  # create a widget
        self.widget.setGeometry(50, 50, 600, 600)  # set widget size
        self.widget.show()  # show the widget
        self.startTime = None
        self.endTime = None

    def startGame(self):  # begins the game
        self.timer = QTimer()  # create the timer
        self.startTime = time.time()  # set game start time
        self.timer.timeout.connect(self.performMove)  # timeout waits on performMove
        self.timer.start(60)  # give 30 seconds for AI to act
        self.showBoard()  # display the board

    def performMove(self):  # makes a move
        if self.game.isEnd() is None:  # if the game isn't over
            self.game.performMove()  # make the Game make a move

        else:  # if the game is over, display winner and how they won
            end = self.game.isEnd()   # get values from isEnd
            self.endTime = time.time()  # get end time
            print(end[0])
            print(end[1])
            strTime = str(timedelta(seconds=(self.endTime - self.startTime)))  # get time passed
            print("Total time: {0}".format(strTime))
            exit()

        self.showBoard()

    def showBoard(self):  # refreshes the board in the GUI
        # str representation of the svg board, should be flipped if human player is p2
        boardUI = chess.svg.board(self.game.board, flipped=self.game.flipped)
        uiBytes = QByteArray()  # create a byte array for the widget
        uiBytes.append(boardUI)  # add the board to the byte array
        self.widget.load(uiBytes)  # load the widget to display the updated board


try:
    # create the players
    # p1 - white, p2 - black
    # AI options - beginner, intermediate, expert
    player1 = HumanPlayer()
    player2 = AIPlayer("intermediate")

    gameBoard = chess.Board()  # create a new board for the game
    chessGame = Game(gameBoard, [player1, player2])  # create a new game object - give board and players
    gui = GUI(chessGame)  # create a new gui object - give the game object

    gui.startGame()  # start the game
    sys.exit(gui.app.exec_())  # do not end the game until the GUI closes
finally:
    print()
