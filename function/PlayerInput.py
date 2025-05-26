import pygame

class PlayerInput:
    
    def __init__(self,m):
        self.RESET(m)
    
    def main(self,m):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                m.stop()
    
    def RESET(self,m):
        
        pass