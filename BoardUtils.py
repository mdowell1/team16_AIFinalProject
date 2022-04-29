import math
import random
import time
import chess
import chess.polyglot
import chess.pgn
import PieceSquare
import ZobristHash

# region variables
p = 1  # pawn
nb = 3  # knight and bishop
r = 5  # rook
q = 9  # queen
k = 10000  # king
seen = 0
movesData = {}
seenBoards = {}
Hash = ZobristHash.Hash()
hit = 0
miss = 0
inEnd = False


# endregion

# region evaluationFunction

#  calls other functions to get material, control, and mobility values
#  weighs these values, adds them, and returns them
def EvalFunc(board: chess.Board, parentHash):
    curHash = Hash.getHash(board, parentHash)  # get hash value of current board
    cachedVal = Hash.hasHash(curHash)  # see if board is in the hash table
    global hit, miss
    if cachedVal is not None:  # if board is in hash table
        hit = hit + 1  # update hits
        return cachedVal[1]  # return the cached value
    else:
        legalMoves = GetLegalMoves(board)  # get mobility
        materialVals = GetPieceVals(board)  # get material
        locationVals = GetLocationVals(board)  # get control
        miss = miss + 1  # update misses

    # always white - black
    mobility = legalMoves[1] - legalMoves[
        0]  # other player - this player -> neg if cur is in lead, pos if not, getting net mobility value
    material = materialVals[1] - materialVals[0]  # getting the net material value
    control = locationVals[1] - locationVals[0]  # getting the net control value
    # get weighted values and return the combined value - material is more important than other items
    weighted = (0.05 * mobility) + (0.1 * control) + (2 * material)  # + (0.08 * freqVal)
    Hash.updateTable(curHash, [0, weighted])
    return weighted


# gets number of legal moves for each player
def GetLegalMoves(board: chess.Board) -> [int, int]:
    legalMovesCurPlayer = len(list(board.legal_moves))  # number of moves this player can take
    board.turn = 1 - board.turn  # switch the board turn to the other player to get their legal moves
    legalMovesOtherPlayer = len(list(board.legal_moves))  # number of moves other player can take
    board.turn = 1 - board.turn  # switch back to this player so they can act

    # always return values in order of black, white
    if board.turn == 0:
        return legalMovesCurPlayer, legalMovesOtherPlayer
    return legalMovesOtherPlayer, legalMovesCurPlayer


# adds the values of each piece the players have on board
def GetPieceVals(board: chess.Board) -> [int, int]:
    boardStr = str(board)  # get a string representation of the board

    # for both players, add the value of each piece they have on the board
    whiteVal = (k * boardStr.count('K')) + (q * boardStr.count('Q')) + (r * boardStr.count('R')) + (
            nb * (boardStr.count('B') + boardStr.count('N'))) + (p * boardStr.count('P'))
    blackVal = (k * boardStr.count('k')) + (q * boardStr.count('q')) + (r * boardStr.count('r')) + (
            nb * (boardStr.count('b') + boardStr.count('n'))) + (p * boardStr.count('p'))

    return [blackVal, whiteVal]  # return values


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
            if inEndGame(board):
                whiteVal += PieceSquare.pieceSquareTableWhite.get('KE')[i]
            else:
                whiteVal += PieceSquare.pieceSquareTableWhite.get('KM')[i]
        elif piece.symbol() == 'k':  # k is the king for the black side
            if inEndGame(board):
                blackVal += PieceSquare.pieceSquareTableBlack.get('KE')[i]
            else:
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

    return [blackVal, whiteVal]  # return values


# returns if players are in the end game
def inEndGame(board):
    global inEnd
    if not inEnd:  # if the current value is false, check if it's still the case
        strBoard = str(board).lower()
        if strBoard.count('p') == 0:  # if no more pawns, in end game
            inEnd = True
        elif strBoard.count('q') < 2:  # if at least 1 queen is gone, in end game
            inEnd = True
        elif strBoard.count('q') > 0 and strBoard.count('p') < 4:  # if there is a queen and few pawns left, in end game
            inEnd = True

    return inEnd  # return if board is in end game


# endregion

# region MiniMax
def MiniMaxRoot(board, depth):
    global seen
    isMax = board.turn  # white maximizing, black minimizing
    alpha = -math.inf  # initialize alpha and beta
    beta = math.inf
    possible = []  # create empty list of possible moves
    hashVal = Hash.getHash(board)  # get the hash value for this board
    moves = GetOrderedMoves(board)  # get sorted moves

    # loop through each legal move
    for m in moves:
        board.push(m)  # make the move
        seen += 1  # debugging - increase num of seen boards

        # call the MiniMax function and get the value from traversing the tree after making the move
        val = MiniMax(depth, 1 - isMax, board, alpha, beta, hashVal)
        board.pop()  # undo the move
        if isMax:
            if val > alpha:  # since user is maximizing - if value is better than current alpha
                alpha = val  # update the alpha
                possible.clear()  # clear the list of possible moves
                possible.append(m)  # add this to the list of possible moves
            elif val == alpha:  # if the value is the same as the current alpha
                possible.append(m)  # add this to the list of possible moves
        else:
            if val < beta:  # since user is maximizing - if value is better than current alpha
                beta = val  # update the alpha
                possible.clear()  # clear the list of possible moves
                possible.append(m)  # add this to the list of possible moves
            elif val == beta:  # if the value is the same as the current alpha
                possible.append(m)  # add this to the list of possible moves

    print("Seen: {0}".format(seen))
    if len(possible) == 1:  # if only 1 move option, return it
        return possible[0]

    possibleVals = []
    for m in possible:  # loop through all possible moves (have the same evaluation)
        possibleVals.append([m, GetEstimate(board, m)])  # add the move with its estimate to list
    possibleVals.sort(key=lambda x: x[1], reverse=True)  # sort the new list by the estimate for each move
    possible.clear()  # clear the old list of possible moves

    # get the estimate from the first move in the list - this is the highest estimate value
    lastVal = possibleVals[0][1]
    for i in possibleVals:  # loop through each possible move from the new list
        # if this move's estimate is less than the current highest, all remaining moves have a lower value than the highest
        # break out of loop
        if i[1] < lastVal:
            break
        possible.append(i[0])  # if it has the same value as the current highest, add it to the list of possible moves

    return random.choice(possible)  # return a random move from the list of possible moves, all have the same value


# returns a value using MiniMax with AB Pruning
def MiniMax(depth, isMax, board, alpha, beta, prevHash):
    global seen, hit
    seen += 1  # debugging - increase number of seen boards

    if depth == 0:  # if search depth is reached
        return EvalFunc(board, prevHash)  # return the value of the current board

    prevHash = Hash.getHash(board, prevHash)  # get hash value of this board
    cachedVal = Hash.hasHash(prevHash)  # see if board is cached
    if cachedVal is not None:  # if it is cached
        if cachedVal[0] >= depth:  # see if cached depth is acceptable
            hit = hit + 1  # if it is, update hits and return the cached value
            return cachedVal[1]

    if isMax:  # if currently maximizing
        moves = GetOrderedMoves(board)  # get list of legal moves
        best = -math.inf  # initialize value to beat
        for m in moves:  # loop through legal moves
            board.push(m)  # make the move
            # recursively call minimax and get the value for child tree
            val = MiniMax(depth - 1, False, board, alpha, beta, prevHash)  # not maximizing for child
            board.pop()  # undo the move
            best = max(best, val)  # update best if returned value is larger than current best value
            alpha = max(alpha, best)  # update alpha if best value is larger than current alpha

            if beta <= alpha:  # if alpha value has surpassed or met beta value
                break  # do not continue - prune tree

    else:  # if currently minimizing
        moves = GetOrderedMoves(board)  # get list of legal moves
        best = math.inf  # initialize value to beat
        for m in moves:  # loop through legal moves
            board.push(m)  # make the move
            # recursively call minimax and get the value for child tree
            val = MiniMax(depth - 1, True, board, alpha, beta, prevHash)  # maximizing for child
            board.pop()  # undo the move
            best = min(best, val)  # update best if returned value is less than current best value
            beta = min(beta, best)  # update beta if best value is less than current beta

            if beta <= alpha:  # if beta has met or passed alpha value
                break  # do not continue - prune tree

    Hash.updateTable(prevHash, [depth, best])  # update hash table with new board evaluation
    return best  # return best value


# endregion

# region book moves and sorting

# gets and returns an opening book move if one is available
def GetPolyglotMove(board: chess.Board):
    # read the bin file of opening book moves
    with chess.polyglot.open_reader("data/Performance.bin") as reader:
        b = reader.get(board)  # provide the current board and get a move
        if b is not None:  # if there is a move, return it
            return b.move
        else:  # otherwise, return none
            return None


# sort by estimate
def GetOrderedMoves(board: chess.Board):
    def order(move):  # returns estimate for move
        return GetEstimate(board, move)

    # sorts the legal moves by order given above, reverses so higher values are first
    moves = sorted(board.legal_moves, key=order, reverse=True)
    return moves  # return the sorted moves


# https://stackoverflow.com/questions/61778579/what-is-the-best-way-to-find-out-if-the-move-captured-a-piece-in-python-chess
# get evaluation estimate
def GetEstimate(board: chess.Board, move: chess.Move) -> int:
    global inEnd
    boardEval = 0

    if board.is_en_passant(move):  # add 1 if move is en passant capture - these are not included in is_capture
        boardEval += 1
    elif board.is_capture(move):  # add value of captured piece if move is a capture
        boardEval = board.piece_at(move.to_square).piece_type
    if board.is_castling(
            move):  # add 1 if move is castling - affects final decision, but not the actual board evaluation
        boardEval += 1
    if board.gives_check(
            move):  # add 1 if move gives a check - affects final decision, but not the actual board evaluation
        boardEval += 1
    # add 1 if piece moved is a pawn and players are in the end game - encourages pushing passed pawns
    # affects final decision, but not the actual board evaluation
    if board.piece_at(move.from_square).piece_type == 1 and inEnd:
        boardEval += 1
    return boardEval  # return final evaluation estimate


# endregion


# given a board and a depth, returns a move for the AI to make
def GetMove(board, depth):
    move = GetPolyglotMove(board)  # first try to get a book move

    if move is None:  # if there wasn't a book move to use
        move = MiniMaxRoot(board, depth)  # get the move using minimax with AB Pruning
    else:
        time.sleep(1)  # make it look like the AI is thinking rather than immediately making a move - was not included in testing
    return move  # return the move
