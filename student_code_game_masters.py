from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state = []
        peg1 = []
        peg2 = []
        peg3 = []
        for fact in self.kb.facts:
            if str(fact.statement) == "(on disk1 peg1)":
                peg1.append(1)
            elif str(fact.statement) == "(on disk2 peg1)":
                peg1.append(2)
            elif str(fact.statement) == "(on disk3 peg1)":
                peg1.append(3)
            elif str(fact.statement) == "(on disk4 peg1)":
                peg1.append(4)
            elif str(fact.statement) == "(on disk5 peg1)":
                peg1.append(5)
            elif str(fact.statement) == "(on disk1 peg2)":
                peg2.append(1)
            elif str(fact.statement) == "(on disk2 peg2)":
                peg2.append(2)
            elif str(fact.statement) == "(on disk3 peg2)":
                peg2.append(3)
            elif str(fact.statement) == "(on disk4 peg2)":
                peg2.append(4)
            elif str(fact.statement) == "(on disk5 peg2)":
                peg2.append(5)
            elif str(fact.statement) == "(on disk1 peg3)":
                peg3.append(1)
            elif str(fact.statement) == "(on disk2 peg3)":
                peg3.append(2)
            elif str(fact.statement) == "(on disk3 peg3)":
                peg3.append(3)
            elif str(fact.statement) == "(on disk4 peg3)":
                peg3.append(4)
            elif str(fact.statement) == "(on disk5 peg3)":
                peg3.append(5)

        peg1.sort()
        peg2.sort()
        peg3.sort()
        state.append(tuple(peg1))
        state.append(tuple(peg2))
        state.append(tuple(peg3)) 
        return (tuple(state))        
        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        
        ### Student code goes here

        ### move to another peg
        ## need to
        statement = str(movable_statement).split()
        disk = statement[1]
        pegfrom = statement[2]
        pegfromNum = int(pegfrom[-1]) -1 
        pegto = statement[3] 
        pegto = pegto[:-1]
        pegtoNum = int(pegto[-1]) -1 

        currentState = self.getGameState()
        pegfromTuple = currentState[pegfromNum]
        pegtoTuple = currentState[pegtoNum]

        #retract disk on pegfrom
        #retract top disk pegfrom
        
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + pegfrom + ")"))
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + pegfrom + ")"))
        
        #if pegfrom only has one element:
        if len(pegfromTuple) == 1:
            #assert empty peg
            self.kb.kb_assert(parse_input("fact: (empty " + pegfrom + ")"))
        else:
            #assert (top (2ndToLast) fromPeg)
            self.kb.kb_assert(parse_input("fact: (top disk" + str(pegfromTuple[1])  + " "+ pegfrom + ")"))
            #retract (onTopOf disk (2ndToLast))
            self.kb.kb_retract(parse_input("fact: (onTopOf " + disk + " disk" + str(pegfromTuple[1]) + ")"))

        if len(pegtoTuple) == 0:
            self.kb.kb_retract(parse_input("fact: (empty " + pegto + ")"))
        else:
            #retract (top (last element) toPeg)
            self.kb.kb_retract(parse_input("fact: (top disk" + str(pegtoTuple[0]) + " " + pegto + ")"))
            #assert (onTopOf disk (oldtop))
            self.kb.kb_assert(parse_input("fact: (onTopOf " + disk + " disk"+ str(pegtoTuple[0]) + ")"))

        #normal
        #assert (top disk pegTo)
        self.kb.kb_assert(parse_input("fact: (top " + disk + " "+ pegto + ")"))
        #assert (on disk pegTo)
        self.kb.kb_assert(parse_input("fact: (on " + disk + " "+ pegto + ")"))

            
        
        
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        state = []
        row1 = []
        row2 = []
        row3 = []
        rows = [[], row1, row2, row3]
        

        for i in range(1, 4):
            for j in range(1, 4):
                currCell = self.kb.kb_ask(parse_input("fact: (coordinate ?x pos" +str(j) + " pos" + str(i) + ")"))
                currtile = str(currCell[0].bindings[0].constant)
                if currtile == "tile1":
                    rows[i].append(1)
                elif currtile == "tile2":
                    rows[i].append(2)
                elif currtile == "tile3":
                    rows[i].append(3)
                elif currtile == "tile4":
                    rows[i].append(4)
                elif currtile == "tile5":
                    rows[i].append(5)
                elif currtile == "tile6":
                    rows[i].append(6)
                elif currtile == "tile7":
                    rows[i].append(7)
                elif currtile == "tile8":
                    rows[i].append(8)
                elif currtile == "tile9":
                    rows[i].append(9)
                elif currtile == "empty":
                    rows[i].append(-1)

        


        state.append(tuple(row1))
        state.append(tuple(row2))
        state.append(tuple(row3))
        return (tuple(state))  


        
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        statement = str(movable_statement).split()
       
        tile = statement[1]
        fromPos = statement[2] + " " + statement[3]
        toPos = statement[4] + " " + statement[5][:-1]

        #retract tile from old pos
        #print("fact: (coordinate " + tile + " " + fromPos + ")")
        self.kb.kb_retract(parse_input("fact: (coordinate " + tile + " " + fromPos + ")"))
        #retract empty from new pos
        #print("fact: (coordinate empty " + toPos + ")")
        self.kb.kb_retract(parse_input("fact: (coordinate empty " + toPos + ")"))
        #assert new position of empty tile
        #print("fact: (coordinate empty " + fromPos + ")")
        self.kb.kb_assert(parse_input("fact: (coordinate empty " + fromPos + ")"))
        #assert new position of moved tile
        #print("fact: (coordinate " + tile + " " + toPos + ")")
        self.kb.kb_assert(parse_input("fact: (coordinate " + tile + " " + toPos + ")"))
        


        
        ### Student code goes here



        
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
