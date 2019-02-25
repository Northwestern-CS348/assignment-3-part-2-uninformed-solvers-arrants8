
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)



        
    
    def solveOneStep(self):
        if self.currentState.state == self.victoryCondition:
            return True

        else:
            #get the possible next moves
            
            possibleMoves = self.gm.getMovables()
            current = self.currentState
            
            #if there are possible moves
            if possibleMoves:
                for move in possibleMoves:
                    #make child move
                    self.gm.makeMove(move)
                    new_move = GameState(self.gm.getGameState(), current.depth + 1, move)
                    #add this move to children
                    current.children.append(new_move)
                    new_move.parent = current
                    self.gm.reverseMove(move)
                for move in current.children:
                    if move not in self.visited:
                        #if it hasn't been visited, visit it 
                        self.visited[move] = True
                        #make the move and change the current state
                        self.gm.makeMove(move.requiredMovable)
                        self.currentState = move

                        return False

            #if there are no moves
            else:
                self.gm.reverseMove(self.currentState.requiredMovable)

            return False
            

        
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
                ##self.gm.makeMove(move)
               ##self.solveOneStep

        

    


        

        
        print(self.currentState.state)

        if self.gm.getGameState() == self.victoryCondition:
            return True
        
        
        
        #if there are children
        if self.gm.getMovables():
           
           for move in self.gm.getMovables():
                  
               #add unvisted children to the current state
                    print("CURRENT STATE")
                    print(move)
                   #make a (fake) move
                    self.gm.makeMove(move)
                    #add resultant state as a child of the current state
                    new_state = GameState(self.gm.getGameState, self.currentState.depth + 1, move)
                    #set current state as the parent of child state 
                    new_state.parent = self.currentState
                    #set child state as a child of the parent state
                    self.currentState.children.append(new_state)
                    #go back to parent state, with unvisited children attached
                    self.gm.reverseMove(move)
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)

        #this helper starts to explore the children
        next_child = self.nextChild(self.currentState)

        #if we are at the root and have explored all children, we are done 
        if next_child is None:
            return False
        
        self.gm.makeMove(next_child.requiredMovable)
        self.visited[child_to_visit] = True
        updatedState = self.gm.getGameState()
        self.currentState = next_child
        if updatedState == self.victoryCondition:
            return True
        return False





        def nextChild(self, currNode):
            i = currNode.nextChildToVisit
            #if more children to see and not visited, return that child
            if currNode.children[i] not in self.visited and i < len(currNode.children):
                return currNode.children[i]
            #if explored all children, go back. 
            elif index >= len(currNode.children):
                #if we are at the root, return None. we've explored all 
                if currNode.parent is None:
                    return None
                #otherwise, return to parent
                else:
                    self.gm.reverseMove(currNode.requiredMovable)
                    return self.findNextVisitDFS(currNode.parent)
            #if the node was only visited, move to next
            currNode.nextChildToVist += 1
            return self.nextChild(currNode)
                    
                
                
            
            
            

        


        
                
        
            

        
        ### Student code goes here
        return True

         """
class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
