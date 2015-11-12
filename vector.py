import math

class vec2d(object): # this says what to do with lists that have 2 values like (x, y)
    
    def __init__(self, x, y): # splits some (x, y) numbers into seperate numbers
        self.x = x
        self.y = y

    def __sub__(self, other): # subtract
            return vec2d(self.x - other.x, self.y - other.y)
        
    def __repr__(self): # print
        return "(%s, %s)"%(self.x, self.y)

    def __getitem__(self, key): # get one of the values from the vector
        return (self.x, self.y)[key]

    def get_length(self): # gets the length of a vector
        return math.sqrt((self.x**2 + self.y**2)) # equasion to get length

    def normalize(self): # this is dividing something by its length used for direction to move
        length = self.get_length() # gets the length
        if length != 0: # if we are not going to divide by zero
            return(self.x / length, self.y / length) # divides (x, y) by the length
        
        return (self.x, self.y) # if length == 0 then skip the division step
