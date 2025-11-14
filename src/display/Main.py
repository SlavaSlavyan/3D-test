import pygame

class Display:
    
    def __init__(self,m):
        
        self.Screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE)
        
        self.Clock = pygame.time.Clock()
    
    def main(self,m):
        
        self.width, self.height = self.Screen.get_size()
        
        exec(f"m.Scenes.{m.Scenes.id}.Disp.main(m)")
        
        pygame.display.flip()
        
        self.Clock.tick(60)