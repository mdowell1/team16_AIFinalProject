import math
import os.path
import random
import traceback
import chess
import chess.polyglot
import chess.pgn
import pickle
import BoardUtils
import PieceSquare

# values of pieces
p = 1  # pawn
nb = 3  # knight and bishop
r = 5  # rook
q = 9  # queen
k = 10000  # king
seen = 0
movesData = {}
pgnOffsets = []
seenBoards = {}


# region evaluationFunction

#  calls other functions to get material, control, and mobility values
#  weighs these values, adds them, and returns them
def EvalFunc(board: chess.Board):
    # ----- uncomment if used again ---------
    # if len(seenBoards) == 0:
    #   GetSeenBoards()

    # if seenBoards.get(str(board)) is not None:
    #     val = seenBoards[str(board)]
    #     legalMoves = val[0]
    #     materialVals = val[1]
    #     locationVals = val[2]

    # else:
    legalMoves = GetLegalMoves(board)  # get mobility
    materialVals = GetPieceVals(board)  # get material
    locationVals = GetLocationVals(board)  # get control
    seenBoards[str(board)] = [legalMoves, materialVals, locationVals]

    playerNum = board.turn
    mobility = legalMoves[1 - playerNum] - legalMoves[
        playerNum]  # other player - this player -> neg if cur is in lead, pos if not, getting net mobility value
    material = materialVals[1 - playerNum] - materialVals[
        playerNum]  # getting the net material value
    control = locationVals[1 - playerNum] - locationVals[
        playerNum]  # getting the net control value

    # --------- uncomment if used again -----------
    # get how common the move is at this point in time
    # always positive, adds to the current player's weight
    #    frequencies = MoveFrequencyWeight(board)
    #   approx = frequencies[0]
    #  exact = frequencies[1]
    # freqVal = (approx * .3) + (exact * .7)

    # get weighted values and return the combined value - material is more important than other items
    weighted = (0.05 * mobility) + (0.1 * control) + (0.85 * material)  # + (0.08 * freqVal)
    return weighted


# gets number of legal moves for each player
def GetLegalMoves(board: chess.Board) -> [int, int]:
    legalMovesCurPlayer = len(list(board.legal_moves))  # number of moves this player can take
    board.turn = 1 - board.turn  # switch the board turn to the other player to get their legal moves
    legalMovesOtherPlayer = len(list(board.legal_moves))  # number of moves other player can take
    board.turn = 1 - board.turn  # switch back to this player so they can act

    # return values in order of black, white
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

    return [blackVal, whiteVal]  # return values


# endregion

# region MiniMax


# not currently in use
# returns a move using MiniMax without AB Pruning
def MiniMaxOld(board, depth):  # actions is [board,  val]

    # recursive function to go further into tree
    def recurse(playerNum, curDepth=0):
        localBestVal = EvalFunc(board)  # get the current board value

        if curDepth == depth:  # if we have met the depth
            return localBestVal  # return the board evaluation

        for m in board.legal_moves:  # loop through each legal move
            BoardUtils.seen += 1  # debugging - increase seen boards num
            board.push(m)  # make the move
            newVal = recurse(1 - playerNum, curDepth + 1)  # get the value on child tree after making the move
            board.pop()  # undo the move
            if playerNum == 0:  # if player is Black
                localBestVal = max(localBestVal, newVal)  # get the max of the values
            else:  # if player is white
                localBestVal = min(localBestVal, newVal)  # get the min of the values
        return localBestVal  # return the best value

    moves = board.legal_moves  # get legal moves
    if board.turn == 0:  # if player is Black
        bestVal = -math.inf  # maximizing, set best val
    else:  # if player is white
        bestVal = math.inf  # minimizing, set best val

    bestMove = None  # don't currently know the best move
    try:
        for move in moves:  # loop through each legal move
            BoardUtils.seen += 1  # debugging - increase seen boards
            board.push(move)  # make the move
            if board.turn == 0:  # if player is Black - maximizing
                # call the recurse function and get the max of current and returned value
                val = max(bestVal, recurse(1 - board.turn))
                if val > bestVal:  # if the value is better than the current best val
                    bestMove = move  # this is the best move so far
                    bestVal = val  # this is the best value so farr
            else:  # if player is White - minimizing
                # call the recurse function and get the min of current and returned value
                val = min(bestVal, recurse(1 - board.turn))
                if val < bestVal:  # if the value is better than the current best val
                    bestMove = move  # this is the best move so far
                    bestVal = val  # this is the best value so far
            board.pop()  # undo the move
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    print("Seen: {0}".format(BoardUtils.seen))
    return bestMove  # return the best move to make


# returns a move using MiniMax with AB Pruning
# used with the starting board configuration
def MiniMaxRoot(board, depth):
    # initialize alpha and beta
    alpha = -math.inf
    beta = math.inf
    possible = []  # create empty list of possible moves

    # loop through each legal move
    for m in board.legal_moves:
        board.push(m)  # make the move
        BoardUtils.seen += 1  # debugging - increase num of seen boards

        # call the MiniMax function and get the value from traversing the tree after making the move
        val = MiniMax(depth, False, board, alpha, beta)
        board.pop()  # undo the move
        if val > alpha:  # since user is maximizing - if value is better than current alpha
            alpha = val  # update the alpha
            possible.clear()  # clear the list of possible moves
            possible.append(m)  # add this to the list of possible moves
        if val == alpha:  # if the value is the same as the current alpha
            possible.append(m)  # add this to the list of possible moves

    print("Seen: {0}".format(BoardUtils.seen))
    return random.choice(possible)  # return a random move from the list of possible moves, all have the same value


# returns a value using MiniMax with AB Pruning
def MiniMax(depth, isMax, board, alpha, beta):
    BoardUtils.seen += 1  # debugging - increase number of seen boards

    if depth == 0:  # if search depth is reached
        return EvalFunc(board)  # return the value of the current board

    moves = list(board.legal_moves)  # get list of legal moves
    # random.shuffle(moves)  # may slightly decrease search time

    if isMax:  # if currently maximizing
        best = -math.inf  # initialize value to beat
        for m in moves:  # loop through legal moves
            board.push(m)  # make the move
            # recursively call minimax and get the value for child tree
            val = MiniMax(depth - 1, False, board, alpha, beta)  # not maximizing for child
            board.pop()  # undo the move
            best = max(best, val)  # update best if returned value is larger than current best value
            alpha = max(alpha, best)  # update alpha if best value is larger than current alpha

            if beta <= alpha:  # if alpha value has surpassed or met beta value
                break  # do not continue - prune tree

        return best  # return best value

    else:  # if currently minimizing
        best = math.inf  # initialize value to beat
        for m in moves:  # loop through legal moves
            board.push(m)  # make the move
            # recursively call minimax and get the value for child tree
            val = MiniMax(depth - 1, True, board, alpha, beta)  # maximizing for child
            board.pop()  # undo the move
            best = min(best, val)  # update best if returned value is less than current best value
            beta = min(beta, best)  # update beta if best value is less than current beta

            if beta <= alpha:  # if beta has met or passed alpha value
                break  # do not continue - prune tree

        return best  # return best value


# endregion

# region using files

# gets and returns an opening book move if one is available
def GetPolyglotMove(board: chess.Board):
    # read the bin file of opening book moves
    with chess.polyglot.open_reader("data/Performance.bin") as reader:
        b = reader.get(board)  # provide the current board and get a move
        if b is not None:  # if there is a move, return it
            return b.move
        else:  # otherwise, return none
            return None


# not currently in use
# gets previously-seen boards from txt file
def GetSeenBoards():
    # get if the file exists
    filePath = "data/boards.txt"
    exists = os.path.exists(filePath)

    # if it does exist, open it and read the items
    if exists:
        with open(filePath, 'rb') as file:
            try:
                items = pickle.load(file)
            except:  # if there's an error, make items list empty
                items = {}
    # if it doesn't exist, create it and make items list empty
    else:
        f = open(filePath, 'a')
        items = {}

    BoardUtils.seenBoards = items  # update the seen boards list with the items from the file


# not currently in use
# updates the list of seen boards in the boards file
def AddSeenBoards():
    # if the seen boards list is empty, return
    if len(BoardUtils.seenBoards) == 0:
        return

    filePath = "data/boards.txt"  # record file
    data = {}  # start with empty dict
    exists = os.path.exists(filePath)  # get if the file exists

    # if it doesn't, create the file
    if not exists:
        f = open(filePath, 'a')
    # if it does, open the file and get the dictionary from it
    else:
        with open(filePath, 'rb') as file:
            data = pickle.load(file)

    data.update(BoardUtils.seenBoards)  # add the seen boards dict to the dict from the file

    # update the file with the new dictionary
    # needed previous steps since dump overwrites the file data, cannot append
    with open(filePath, 'wb') as file:
        pickle.dump(data, file)


# not currently in use
# records moves from a set of games and when they occurred in the game
def GetMovesData():
    # pgn contains real games
    pgn = open("data/lichess_db_standard_rated_2015-05.pgn")
    if len(BoardUtils.pgnOffsets) == 0:  # if we don't currently have a list of offsets, get them from the pgn
        GetOffsets("data/lichess_db_standard_rated_2015-05.txt", pgn)

    numGames = 10000  # number of games to get data from
    moveCount = {}  # dictionary of move counts
    gameLocs = random.sample(range(len(BoardUtils.pgnOffsets)),
                             numGames)  # get 10000 random offsets from the offset list

    # loop through each offset
    for i in gameLocs:
        moves = 0  # reset move count
        pgn.seek(BoardUtils.pgnOffsets[i])  # moves iterator to game at this offset in the pgn file
        game = chess.pgn.read_game(pgn)  # reads game at current point in pgn file
        # loop through all of the moves in the game
        for m in game.mainline_moves():
            moves += 1  # increase move count
            if m not in moveCount:  # if the move is not in the list, add it
                moveCount[m] = [moves]  # also add the move number in the game that this occurred on
            else:  # if the move is in the list already
                moveCount[m].append(moves)  # update its list of move numbers with the current move number

    #  mc = Counter(moveCount)
    #  print(mc[chess.Move.from_uci('d2d4')])
    return moveCount  # return the final dictionary


# not currently in use
# for evaluation function - returns the frequency of when a move occurred in
# the example games (moves data dictionary)
def MoveFrequencyWeight(board: chess.Board):
    curMoves = board.fullmove_number  # get how many moves have happened in this game
    if len(BoardUtils.movesData) == 0:  # if movesData dict isn't populated
        BoardUtils.movesData = GetMovesData()  # populate it

    move = board.peek()  # get the last move performed
    atMoves = BoardUtils.movesData[move]  # get the list of when this moved happened in the example games

    if atMoves is None:  # if the move wasn't in the list, return
        return 0, 0

    if curMoves < 13:  # if we are currently in the early game
        countApprox = len([m for m in atMoves if m < 13])  # get how many times move occurred in early game in examples
    else:  # if we are not currently in the early game
        countApprox = len([m for m in atMoves if m > 12])  # get how many times move occurred after early game in examples

    # get how many times move occurred at exact current move count in examples
    countExact = len([m for m in atMoves if m == curMoves])
    return countApprox, countExact  # return the approximate move count and the exact move count


# not currently in use
# pickle info: https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python
# gets and returns the offsets for each game in a given pgn file
# allows games to be accessed based off of their offset instead of in order
def GetOffsets(filePath, pgn):
    exists = os.path.exists(filePath)  # see if the file exists

    # if it does, open it and load the offsets from it
    if exists:
        with open(filePath, 'rb') as file:
            items = pickle.load(file)

    # if it doesn't
    else:
        f = open(filePath, 'a')  # create the file
        items = []  # create empty list for offsets

        # loop until break
        while True:
            offset = pgn.tell()  # get the offset from the current game in pgn
            headers = chess.pgn.read_headers(pgn)  # get the headers from the current game in pgn
            if headers is None:  # if there is no header, there is no game, break out of loop
                break
            items.append(offset)  # add the offset to the list

        # open the file and add the offsets to it
        with open(filePath, 'wb') as file:
            pickle.dump(items, file)

    BoardUtils.pgnOffsets = items  # update the offsets list

# endregion


# given a board and a depth, returns a move for the AI to make
def GetMove(board, depth):
    move = GetPolyglotMove(board)  # first try to get a book move

    if move is None:  # if there wasn't a book move to use
        move = MiniMaxRoot(board, depth)  # get the move using minimax with AB Pruning

    return move  # return the move
