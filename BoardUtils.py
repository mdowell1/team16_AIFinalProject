import chess
import PieceSquare

# values of pieces
p = 1  # pawn
nb = 3  # knight and bishop
r = 5  # rook
q = 9  # queen
k = 10000  # king


#  calls other functions to get material, control, and mobility values
#  weighs these values, adds them, and returns them
def EvalFunc(board: chess.Board):

    # get mobility
    legalMoves = GetLegalMoves(board)
    mobility = legalMoves[0] - legalMoves[1]

    # get material
    materialVals = GetPieceVals(board)
    material = materialVals[0] - materialVals[1]

    # get control
    locationVals = GetLocationVals(board)
    control = locationVals[0] - locationVals[1]

    # print info
    print("\n\n------------ PLAYER: {0} ------------".format(int(board.turn)))
    print("Legal moves for current player: {0}, Legal moves for other player: {1}".format(legalMoves[0], legalMoves[1]))
    print("Mobility: {0}".format(mobility))
    print("Cur material: {0}, Other material: {1}, Cur Net Material: {2}".format(materialVals[0], materialVals[1], material))
    print("Cur loc val: {0}, Other loc val: {1}, Cur Net loc val: {2}".format(locationVals[0], locationVals[1], control))

    # get weighted values and return the combined value - this will be adjusted later
    weighted = (0.1*mobility) + (0.2*control) + (0.7*material)
    return weighted


# gets number of legal moves for each player
def GetLegalMoves(board: chess.Board) -> [int, int]:
    legalMovesCurPlayer = len(list(board.legal_moves))  # number of moves this player can take
    board.turn = 1 - board.turn  # switch the board turn to the other player to get their legal moves
    legalMovesOtherPlayer = len(list(board.legal_moves))  # number of moves other player can take
    board.turn = 1 - board.turn  # switch back to this player so they can act
    return legalMovesCurPlayer, legalMovesOtherPlayer  # return both of the values


# adds the values of each piece the players have on board
def GetPieceVals(board: chess.Board) -> [int, int]:
    whiteVal = 0  # for white side
    blackVal = 0  # for black side

    # loop through the board
    for i in range(0, 64):
        square = chess.SQUARES[i]  # get the square at this location
        piece = board.piece_at(square)  # get the piece at this square

        if piece is None:  # move on if there isn't a piece at this square
            continue

        # for each piece, add that piece's value to the matching player's piece value
        if piece.symbol() == 'K':  # K is the king for the white side
            whiteVal += k
        elif piece.symbol() == 'k':  # k is the king for the black side
            blackVal += k
        elif piece.symbol() == 'Q':
            whiteVal += q
        elif piece.symbol() == 'q':
            blackVal += q
        elif piece.symbol() == 'R':
            whiteVal += r
        elif piece.symbol() == 'r':
            blackVal += r
        elif piece.symbol() == 'B' or piece.symbol() == 'N':
            whiteVal += nb
        elif piece.symbol() == 'b' or piece.symbol() == 'n':
            blackVal += nb
        elif piece.symbol() == 'P':
            whiteVal += p
        elif piece.symbol() == 'p':
            blackVal += p

    if board.turn == 0:  # return white first if this is white's turn
        return [whiteVal, blackVal]

    return [blackVal, whiteVal]  # return black first if this is black's turn


# gets the total "control" value - adds the value of each piece for its location on the board
def GetLocationVals(board: chess.Board):
    whiteVal = 0  # for white side
    blackVal = 0  # for black side

    # loop through the board
    for i in range(0, 64):
        square = chess.SQUARES[i]  # get the square at this location
        piece = board.piece_at(square)  # get the piece at this square

        if piece is None:  # move on if there isn't a piece at this square
            continue

        # for each piece, add that piece's value at this location on the piece square table
        # to the matching player's piece value
        if piece.symbol() == 'K':  # K is the king for the white side
            # KM is for middle-game value, this will be adjusted later to use either this or end-game value
            whiteVal += PieceSquare.pieceSquareTableWhite.get('KM')[i]
        elif piece.symbol() == 'k':  # k is the king for the black side
            blackVal += PieceSquare.pieceSquareTableBlack.get('KM')[i]
        elif piece.symbol() == 'Q':
            whiteVal += PieceSquare.pieceSquareTableWhite.get('Q')[i]
        elif piece.symbol() == 'q':
            blackVal += PieceSquare.pieceSquareTableBlack.get('Q')[i]
        elif piece.symbol() == 'R':
            whiteVal += PieceSquare.pieceSquareTableWhite.get('R')[i]
        elif piece.symbol() == 'r':
            blackVal += PieceSquare.pieceSquareTableBlack.get('R')[i]
        elif piece.symbol() == 'B':
            whiteVal += PieceSquare.pieceSquareTableWhite.get('B')[i]
        elif piece.symbol() == 'b':
            blackVal += PieceSquare.pieceSquareTableBlack.get('B')[i]
        elif piece.symbol() == 'N':
            whiteVal += PieceSquare.pieceSquareTableWhite.get('N')[i]
        elif piece.symbol() == 'n':
            blackVal += PieceSquare.pieceSquareTableBlack.get('N')[i]
        elif piece.symbol() == 'P':
            whiteVal += PieceSquare.pieceSquareTableWhite.get('P')[i]
        elif piece.symbol() == 'p':
            blackVal += PieceSquare.pieceSquareTableBlack.get('P')[i]

    if board.turn == 0:  # return white first if this is white's turn
        return [whiteVal, blackVal]

    return [blackVal, whiteVal]  # return black first if this is black's turn
