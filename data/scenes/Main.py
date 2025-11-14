from data.scenes.game._pack import Pack as Game

class Scenes:
    
    def __init__(self,m):
        self.Game = Game(m)
        
        self.id = 'Game'