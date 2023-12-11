import pygame
import sys
import ast
import random

class Agent:
    """
        Base class for agents.
    """
    
    def __init__(self, index) -> None:
        self.index = index

    def getAction(self, state):
        """
            This method receives a GameState object and returns an action based on its strategy.
        """
        pass

class MouseAgent(Agent):
    
    def __init__(self, index, window_size, **kwargs) -> None:
        super().__init__(index)
        self.window_size = window_size

    def getAction(self, state):

        square_size = self.window_size // 8

        allowed_actions = state.getLegalActions(self.index)
        action = None
        
        while action is None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos[1] // square_size, pos[0] // square_size
                    if (x, y) in allowed_actions:
                        action = (x, y)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        return action
    
class KeyBoardAgent(Agent):

    def __init__(self, index, **kwargs) -> None:
        super().__init__(index)

    def getAction(self, state):
        
        allowed_actions = state.getLegalActions(self.index)

        print('allowed actions:')
        print(allowed_actions)

        action = None

        while action is None:

            temporary_input = input('please choose a tuple from the list above:\t')

            try:
                choice = ast.literal_eval(temporary_input)
            except Exception:
                print('your input must be in shape of a tuple.')
                continue

            if choice not in allowed_actions:
                print('your tuple must be one of the mentioned.')
                continue
            
            action = choice

        return action


class DestroyZeroAgent (Agent):
    def __init__ (O0O0O00O0O000O0O0 ,OOO0OO000O0OO00OO ,depth =1 ,**OOOOO000OO00O0OO0)->None :
        super ().__init__ (OOO0OO000O0OO00OO)
        O0O0O00O0O000O0O0 .depth =depth 
    def getAction (O0O00OOO000OOO000 ,O000O0O0O000OO000):
        _O00OO0OO000OOOO00 ,OO000O00O00OO0OOO =O0O00OOO000OOO000 .fn (O000O0O0O000OO000 ,0 ,O0O00OOO000OOO000 .index)
        return OO000O00O00OO0OOO 
    def fn (OO0OO0O0O0O000O0O ,O0OO0OO0O0000O0O0 ,O00OO00O0O00O0OOO ,OOO0OOOO0OOO0O0OO):
        O0O000O00000OO0O0 =O0OO0OO0O0000O0O0 .getNumAgents ()
        if O0OO0OO0O0000O0O0 .isGameFinished ()or O00OO00O0O00O0OOO ==OO0OO0O0O0O000O0O .depth :
            return (OO0OO0O0O0O000O0O .evaluationFunction (O0OO0OO0O0000O0O0),"")
        OOO0OOO00O0OOOOO0 =O0OO0OO0O0000O0O0 .getLegalActions (OO0OO0O0O0O000O0O .index)
        O0OO0OO000O00O00O =(OOO0OOOO0OOO0O0OO +1)%O0O000O00000OO0O0 
        OO0O00OOO00OOOO0O =(O00OO00O0O00O0OOO +1)if O0OO0OO000O00O00O ==OO0OO0O0O0O000O0O .index else O00OO00O0O00O0OOO 
        if OOO0OOOO0OOO0O0OO ==0 :
            O0000000000O0000O =-999999 
            O0O000000000OOOOO =""
            for O0OOOOOO0O0O00OO0 in OOO0OOO00O0OOOOO0 :
                OOOO000000O0O00OO =O0OO0OO0O0000O0O0 .generateSuccessor (OOO0OOOO0OOO0O0OO ,O0OOOOOO0O0O00OO0)
                OO000O0O0O0O0OO00 ,_O0O0000OOO0OO000O =OO0OO0O0O0O000O0O .fn (OOOO000000O0O00OO ,OO0O00OOO00OOOO0O ,O0OO0OO000O00O00O)
                if OO000O0O0O0O0OO00 >O0000000000O0000O :
                    O0000000000O0000O =OO000O0O0O0O0OO00 
                    O0O000000000OOOOO =O0OOOOOO0O0O00OO0 
        else :
            O0000000000O0000O =999999 
            O0O000000000OOOOO =""
            for O0OOOOOO0O0O00OO0 in OOO0OOO00O0OOOOO0 :
                OOOO000000O0O00OO =O0OO0OO0O0000O0O0 .generateSuccessor (OOO0OOOO0OOO0O0OO ,O0OOOOOO0O0O00OO0)
                OO000O0O0O0O0OO00 ,_O0O0000OOO0OO000O =OO0OO0O0O0O000O0O .fn (OOOO000000O0O00OO ,OO0O00OOO00OOOO0O ,O0OO0OO000O00O00O)
                if OO000O0O0O0O0OO00 <O0000000000O0000O :
                    O0000000000O0000O =OO000O0O0O0O0OO00 
                    O0O000000000OOOOO =O0OOOOOO0O0O00OO0 
        return (O0000000000O0000O ,O0O000000000OOOOO)
    def evaluationFunction (O0OO0OOOOOO00O000 ,OO0OOOOOOOOO00O00):
        ""
        return OO0OOOOOOOOO00O00 .getScore (0)
class MysteriousAgent (Agent):
    def __init__ (OOOO00O0000000O0O ,OO0O00O0O00O0O000 ,depth =1 ,**OOO0O00000OOO0O00)->None :
        super ().__init__ (OO0O00O0O00O0O000)
        OOOO00O0000000O0O .depth =depth 
    def getAction (O0O0OO0O00O0OO000 ,OOO00OO0OO00OO0O0):
        ""
        OO00000OO0OO0O0O0 =float ('inf')
        OO0OO0O0OOO0OO0OO =-OO00000OO0OO0O0O0 
        OO0OOO00OOO00000O =OO00000OO0OO0O0O0 
        _OO0OO0O0000OO0OOO ,OO00OO0000O0OO0OO =O0O0OO0O00O0OO000 .fn_ (OOO00OO0OO00OO0O0 ,0 ,O0O0OO0O00O0OO000 .index ,OO0OO0O0OOO0OO0OO ,OO0OOO00OOO00000O)
        return OO00OO0000O0OO0OO 
    def fn_ (OO0O00O00O00O0000 ,O000OO0OO0OOO0000 ,O0O00O0O0O0OO0OO0 ,OO0O0O000OO000OOO ,OOO0000OO00000OOO ,OOO00OOOOOO0OOO00):
        O0000OO00OOO0O00O =O000OO0OO0OOO0000 .getNumAgents ()
        if O000OO0OO0OOO0000 .isGameFinished ()or O0O00O0O0O0OO0OO0 ==OO0O00O00O00O0000 .depth :
            return (OO0O00O00O00O0000 .evaluationFunction (O000OO0OO0OOO0000),"")
        OOO0O00OO0O0O00O0 =O000OO0OO0OOO0000 .getLegalActions (OO0O0O000OO000OOO)
        OO000000000000O00 =(OO0O0O000OO000OOO +1)%O0000OO00OOO0O00O 
        OOO0O00OOOO00O00O =(O0O00O0O0O0OO0OO0 +1)if OO000000000000O00 ==OO0O00O00O00O0000 .index else O0O00O0O0O0OO0OO0 
        if OO0O0O000OO000OOO ==OO0O00O00O00O0000 .index :
            O0OO0OO0O0OO0OOO0 =-999999 
            O0O00O0OOO00OOO00 =""
            for O0O0O00O0000O0O0O in OOO0O00OO0O0O00O0 :
                O000O0O0O0O0OOO00 =O000OO0OO0OOO0000 .generateSuccessor (OO0O0O000OO000OOO ,O0O0O00O0000O0O0O)
                O0O00000O0OO0OOO0 ,_O0OOOOO0OO0OO0000 =OO0O00O00O00O0000 .fn_ (O000O0O0O0O0OOO00 ,OOO0O00OOOO00O00O ,OO000000000000O00 ,OOO0000OO00000OOO ,OOO00OOOOOO0OOO00)
                if O0O00000O0OO0OOO0 >O0OO0OO0O0OO0OOO0 :
                    O0OO0OO0O0OO0OOO0 =O0O00000O0OO0OOO0 
                    O0O00O0OOO00OOO00 =O0O0O00O0000O0O0O 
                if O0OO0OO0O0OO0OOO0 >OOO00OOOOOO0OOO00 :
                    return (O0OO0OO0O0OO0OOO0 ,"")
                OOO0000OO00000OOO =O0OO0OO0O0OO0OOO0 if O0OO0OO0O0OO0OOO0 >OOO0000OO00000OOO else OOO0000OO00000OOO 
            return (O0OO0OO0O0OO0OOO0 ,O0O00O0OOO00OOO00)
        else :
            O0OO0OO0O0OO0OOO0 =999999 
            O0O00O0OOO00OOO00 =""
            for O0O0O00O0000O0O0O in OOO0O00OO0O0O00O0 :
                O000O0O0O0O0OOO00 =O000OO0OO0OOO0000 .generateSuccessor (OO0O0O000OO000OOO ,O0O0O00O0000O0O0O)
                O0O00000O0OO0OOO0 ,_O0OOOOO0OO0OO0000 =OO0O00O00O00O0000 .fn_ (O000O0O0O0O0OOO00 ,OOO0O00OOOO00O00O ,OO000000000000O00 ,OOO0000OO00000OOO ,OOO00OOOOOO0OOO00)
                if O0O00000O0OO0OOO0 <O0OO0OO0O0OO0OOO0 :
                    O0OO0OO0O0OO0OOO0 =O0O00000O0OO0OOO0 
                    O0O00O0OOO00OOO00 =O0O0O00O0000O0O0O 
                if O0OO0OO0O0OO0OOO0 <OOO0000OO00000OOO :
                    return (O0OO0OO0O0OO0OOO0 ,"")
                OOO00OOOOOO0OOO00 =O0OO0OO0O0OO0OOO0 if O0OO0OO0O0OO0OOO0 <OOO00OOOOOO0OOO00 else OOO00OOOOOO0OOO00 
            return (O0OO0OO0O0OO0OOO0 ,O0O00O0OOO00OOO00)
    def evaluationFunction (O0OOOOOO00000O0O0 ,OOOOO0OOOOOO0OO0O):
        ""
        return OOOOO0OOOOOO0OO0O .getScore (O0OOOOOO00000O0O0 .index)
class IntentionallyBadAtGameAgent (MysteriousAgent):
    def __init__ (OO0OOOOOOO0OOOOO0 ,OO00OOO0OO0OO0OO0 ,**O0OOOOOOOOOO0O000)->None :
        super ().__init__ (OO00OOO0OO0OO0OO0 ,**O0OOOOOOOOOO0O000)
    def getAction (O00000OO00OO00OOO ,O0OOOO0OOOOO00O0O):
        ""
        O0O00OO0000O000OO =float ('inf')
        O00OOO0OO0O000OO0 =-O0O00OO0000O000OO 
        O0000OOOOO0O0O0OO =O0O00OO0000O000OO 
        _O00O000O0OO0O0OOO ,O0OO0OOOO0OOO0OOO =O00000OO00OO00OOO .fn_ (O0OOOO0OOOOO00O0O ,0 ,O00000OO00OO00OOO .index ,O00OOO0OO0O000OO0 ,O0000OOOOO0O0O0OO)
        O0O0O0O0O0O00OOOO =O0OOOO0OOOOO00O0O .getLegalActions (O00000OO00OO00OOO .index)
        if len (O0O0O0O0O0O00OOOO)>1 :
            O0O0O0O0O0O00OOOO .remove (O0OO0OOOO0OOO0OOO)
        return random .choice (O0O0O0O0O0O00OOOO)
class PartiallyRandomAgent (MysteriousAgent):
    def __init__ (OOOO00000O0OO000O ,O00OO000OOOOOO000 ,**O0OO0OO0OOO0OOO0O)->None :
        super ().__init__ (O00OO000OOOOOO000 ,**O0OO0OO0OOO0OOO0O)
    def getAction (OO0O0OOO00O000O0O ,OOO000O0000O00000):
        ""
        if random .random ()>0.25 :
            OO000O0O0OOO0OO0O =float ('inf')
            OO0O0O0O0O0O00OO0 =-OO000O0O0OOO0OO0O 
            O00000OO0OOOOO0O0 =OO000O0O0OOO0OO0O 
            _O0OO00O00O00O0000 ,O0O000OOO00O00O0O =OO0O0OOO00O000O0O .fn_ (OOO000O0000O00000 ,0 ,OO0O0OOO00O000O0O .index ,OO0O0O0O0O0O00OO0 ,O00000OO0OOOOO0O0)
        else :
            O00O00OOO0OOOOO00 =OOO000O0000O00000 .getLegalActions (OO0O0OOO00O000O0O .index)
            O0O000OOO00O00O0O =random .choice (O00O00OOO0OOOOO00)
        return O0O000OOO00O00O0O 