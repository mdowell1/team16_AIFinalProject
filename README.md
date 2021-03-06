# team16_AIFinalProject
Repo for CS 7375 Artificial Intelligence final project (Chess AI)


To play: Run Game.py.  The UI is available to view the board, but will be frozen while awaiting user input - it's helpful to keep the console on one side of the screen and the UI on the other side.

Current implementation:
  - User can play as black by switching player1 and player2 in Game.py
  - AI difficulty can be changed by changing "intermediate" to "beginner" or "expert" in line 89 of Game.py
  - AI uses MiniMax, Alpha-Beta Pruning, Sorting, and an Evaluation Function to make a decision
  - User can move by typing in the 'from' square and the 'to' square, such as "d2d3"
  - Pawns can be promoted by doing the above and appending the piece to promote to, such as "d7d8r" to promote a pawn to a rook

Files:
  - BoardUtils.py - Evaluation function and its supporting functions, sorting implementation, and MiniMax with Alpha-Beta Pruning implementation
  - Game.py - Game and GUI classes for game progression/ending and UI respectively
  - PieceSquare.py - contains dictionaries of piece square values, indicating position values for each piece
  - Players.py - classes for human player and AI player - contains "move" functions to allow players to take an action
  - ZobristHash.py - contains implementation of Zobrist hashing for board caching/hash table

References:
  - Piece-Square Tables - https://www.chessprogramming.org/Simplified_Evaluation_Function
  - PyQt5 usage (for GUI) - https://www.cs.dartmouth.edu/~devin/cs76/03_chess/chess.html
  - python-chess documentation - https://buildmedia.readthedocs.org/media/pdf/python-chess/latest/python-chess.pdf

Any code from references have been commented/adjusted to fit project needs. 
