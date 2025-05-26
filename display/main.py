import pygame

class Display:
    
    def __init__(self,m):
        self.RESET(m)
    
    def main(self,m):
        pass
    
    def load_screen(self,m):
        
        if m.config['full-screen']:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            
        else:
            self.screen = pygame.display.set_mode((m.config['start-size'][0], m.config['start-size'][1]), pygame.RESIZABLE | pygame.DOUBLEBUF)
    
    def RESET(self,m):
        
        self.width, self.height = m.config['start-screen-size']