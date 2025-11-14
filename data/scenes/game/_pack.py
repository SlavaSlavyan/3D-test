from data.scenes.game.Display import Display
from data.scenes.game.Function import Function
from data.scenes.game.Objects import Objects

class Pack:
    
    def __init__(self,m):
        
        self.Objects = Objects()
        
        self.Objects.create_new_object(
            "TEST",
            [
                [0.0,0.0,0.0],
                [1.0,0.0,0.0],
                [0.0,1.0,0.0]
            ],
            [
                [0,1,2]
            ],
            [0.,0.,2.],
            [0.,0.,0.]
        )
        
        self.Disp = Display(m)
        self.Func = Function(m)