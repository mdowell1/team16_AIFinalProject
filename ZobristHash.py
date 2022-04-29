import random


class Hash:
    def __init__(self):
        # gets a random value for each piece (range 12) for each square on the board (range 64)
        self.randHash = [[random.randint(1, 2 ** 64 - 1) for i in range(12)] for j in range(64)]
        self.hashTable = {}  # initialize empty hash table

    # gets the hash value for the provided table
    def getHash(self, board, prevHash=0):
        hashVal = prevHash  # start with given previous hash
        if hashVal == 0:  # if no value is provided
            for i in range(64):  # look through each board square
                piece = board.piece_at(i)  # get the piece at this square
                pieceNum = pieceIndex(piece)  # get the index in the randHash list where the piece is found
                if pieceNum is not None:  # if there is a piece at this position
                    hashVal ^= self.randHash[i][pieceNum]  # update the hash value to include this piece at this position
        else:  # if there is a previous hash value provided
            lastMove = board.peek()  # get last move made
            fromSquare = lastMove.from_square  # get square piece moved from
            toSquare = lastMove.to_square  # get square piece moved to
            piece = board.piece_at(toSquare)  # get the piece that was moved
            # update hash value using xor for the start and end squares using the piece that was moved
            hashVal ^= self.randHash[fromSquare][pieceIndex(piece)]
            hashVal ^= self.randHash[toSquare][pieceIndex(piece)]

        return hashVal  # return the final value

    # returns the value for the given key if available
    def hasHash(self, hashVal):
        if hashVal in self.hashTable:  # if key is in hash table
            return self.hashTable[hashVal]  # return value
        return None  # if not found, return none

    def updateTable(self, hashVal, info):
        self.hashTable[hashVal] = info


# gets the index for each piece to get its value in the  board
def pieceIndex(piece):
    piece = str(piece)
    if piece == 'P':
        return 0
    if piece == 'N':
        return 1
    if piece == 'B':
        return 2
    if piece == 'R':
        return 3
    if piece == 'Q':
        return 4
    if piece == 'K':
        return 5
    if piece == 'p':
        return 6
    if piece == 'n':
        return 7
    if piece == 'b':
        return 8
    if piece == 'r':
        return 9
    if piece == 'q':
        return 10
    if piece == 'k':
        return 11
    return None
