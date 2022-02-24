# team16_AIFinalProject
Repo for CS 7375 Artificial Intelligence final project (Chess AI)


To play: Run Game.py.  The UI is available to view the board, but will be frozen while awaiting user input - it's helpful to keep the console on one side of the screen and the UI on the other side.

Currently has a baseline implementation:
  - User can play as black by switching player1 and player2 in Game.py
  - AI only chooses random moves
  - An evaluation function is in place and called before every board movement, but is not yet finalized and is not currently used in decision-making

Files:
  - BoardUtils.py - Evaluation function and its supporting functions
  - Game.py - Game and GUI classes for game progression/ending and UI respectively
  - PieceSquare.py - contains dictionaries of piece square values, indicating position values for each piece
  - Players.py - classes for human player and AI player - currently only contains "move" functions to allow players to take an action

References:
  - Piece-Square Tables - https://www.chessprogramming.org/Simplified_Evaluation_Function
  - PyQt5 usage (for GUI) - https://www.cs.dartmouth.edu/~devin/cs76/03_chess/chess.html
  - python-chess documentation - https://buildmedia.readthedocs.org/media/pdf/python-chess/latest/python-chess.pdf

Code from references have been commented/adjusted to fit project needs. 
References are also in the code where they are used.
