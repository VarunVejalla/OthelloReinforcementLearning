leftShifts = [0, 0, 0, 0, 1, 9, 8, 7]
rightShifts = [1, 9, 8, 7, 0, 0, 0, 0]

class Board():
    #0 is at topleft corner
    #63 is at bottom right corner
    #topleft is then least significant bit
    #bitboard[index] = value in bitboard counting from right at index
    
    #numTrues(maxTiles) + numTrues(minTiles) = total
    #numTrues(minTiles) = total-numTrues(maxTiles)
    #numTrues(maxTiles) - numTrues(maxTiles) = 2*numTrues(maxTiles) - total
    
    
    def __init__(self, maxTiles, minTiles, total):
        #maxTiles = bitboard for where maxPlayer is
        #minTiles = bitboard for where minPlayer is
        #total is total number of tiles placed so far
        self.maxTiles = maxTiles
        self.minTiles = minTiles
        self.total = total
    
    def occTiles(self):
        #returns bitboard for occupied tiles
        return self.maxTiles|self.minTiles
    
    def unoccTiles(self):
        #returns bitboard for unoccupied tiles
        return ~(self.maxTiles|self.minTiles) & maxSize
    
    def value(self, bitboard, index):
        #returns bitboard[index] (either 0 or 1)
        return (bitboard >> index) & 1
    
    def numTrues(self, bitboard):
        m1  = 0x5555555555555555
        m2  = 0x3333333333333333
        m4  = 0x0f0f0f0f0f0f0f0f
        
        x = bitboard - ((bitboard >> 1) & m1)
        x = (x & m2) + ((x >> 2) & m2)
        x = (x + (x >> 4)) & m4
#        print(x)
        x += x >>  8
        x += x >> 16
        
        x += x >> 32
        return x & 0x7f
    
    def shift(self, bitboard, direction):
        if direction < 4:
            return (bitboard >> rightShifts[direction]) & masks[direction]
        else:
            return (bitboard << leftShifts[direction]) & masks[direction]
#        
#    
    def getScoreMargin(self):
        return 2*self.numTrues(self.maxTiles) - self.total
    
    def move(self, index):
        #returns the copy of Board if maxPlayer plays at index
        new_disk = oneShift[index]
        captured = 0
        newMaxTiles = self.maxTiles|new_disk
        
        for direction in range(4):
            t = masks[direction] & self.minTiles
            x = (new_disk >> rightShifts[direction]) & t
            
            for i in range(5):
                x |= (x >> rightShifts[direction]) & t
            
            bound = (x >> rightShifts[direction]) & masks[direction] & self.maxTiles
            if bound:
                captured |= x
        
        for direction in range(5, 8):
            t = masks[direction] & self.minTiles
            x = (new_disk << leftShifts[direction]) & t
            
            for i in range(5):
                x |= (x << leftShifts[direction]) & t
            
            bound = (x << leftShifts[direction]) & masks[direction] & self.maxTiles
            if bound:
                captured |= x
        
        return Board(self.minTiles^captured, newMaxTiles^captured, self.total + 1)
    
    def validMoves(self):
        
        
        empty = self.unoccTiles()
        valid = 0
        for direction in range(8):
            x = self.shift(self.maxTiles, direction) & self.minTiles
            for i in range(5):
                x |= self.shift(x, direction) & self.minTiles
            
            valid |= self.shift(x, direction) & empty
        
        return valid
    
    def isOver(self):
        return self.maxTiles == 0 or self.minTiles == 0 or self.total == 64
    
    def nextMoves(self, vm):
        #returns a generator for index played at and new Board object
#        vm = self.validMoves()
        index = 0
        while vm:
            lastBit = vm&1
            if lastBit == 1:
                yield index, self.move(index)
            
            vm >>= 1
            index += 1
