import pygame
import sys

class Main:
    
    def __init__(self):
        self.RESET()
        
    def main(self):
        
        pygame.display.flip()
    
    def stop(self):
        
        pygame.quit()
        sys.exit()
    
    def RESET(self):
        
        from JsonManager import JsonManager
        from display.main import Display
        
        pygame.init()
        
        self.JsonManager = JsonManager()
        self.config = self.JsonManager.load("data\\config")
        
        self.Disp = Display(self)